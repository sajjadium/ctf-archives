#include "hypercall.h"

void hp_handle(VM *vm, uint32_t *res) {
  if(vm->run->io.direction == KVM_EXIT_IO_OUT) {
    switch (vm->run->io.port) {
      case HP_RAND:
        *res = hp_rand(vm);
        break;
      case HP_TIME:
        *res = hp_time(vm);
        break;
      case HP_READ:
        *res = hp_read(vm);
        break;
      case HP_WRITE:
        *res = hp_write(vm);
        break;
      case HP_EXIT:
        hp_exit(vm);
        break;
      case HP_DIGEST_GENERATE:
        *res = hp_digestGenerate(vm);
        break;
      case HP_SIGNATURE_VALIDATE:
        *res = hp_signatureValidate(vm);
        break;
      case HP_APPLET_REGISTER_VALIDATE:
        *res = hp_appletRegisterValidate(vm);
        break;
      case HP_APPLET_INVOKE:
        *res = hp_appletInvoke(vm);
        break;
      case HP_APPLET_RESUME:
        *res = hp_appletResume(vm);
        break;
      case HP_APPLETSPACE_FLAG:
        *res = hp_appletspaceFlag(vm);
        break;
      case HP_USERSPACE_FLAG:
        *res = hp_userspaceFlag(vm);
        break;
      case HP_KERNELSPACE_FLAG:
        *res = hp_kernelspaceFlag(vm);
        break;
      default:
        printError("hp_handle::invalid hypercall");
    }
  } else {
    *(uint32_t*)((uint8_t*)vm->run + vm->run->io.data_offset) = *res;
  }
  return;
}

uint64_t getMem(VM *vm, uint32_t paddr, uint32_t size, void *dst) {
  if (paddr >= MEM_SIZE) return FAIL;
  memcpy(dst, &(((char*)vm->mem)[paddr]), size);
  return SUCCESS;
}

uint64_t setMem(VM *vm, uint32_t paddr, uint32_t size, void *src) {
  if (paddr >= MEM_SIZE) return FAIL;
  memcpy(&(((char*)vm->mem)[paddr]), src, size);
  return SUCCESS;
}

uint64_t getHpArg(VM *vm, uint32_t size, void *res) {
  uint32_t paddr = *(uint32_t*)((uint8_t*)vm->run + vm->run->io.data_offset);
  if (getMem(vm, paddr, size, res) == FAIL) return FAIL;
  return SUCCESS;
}

uint64_t setHpArgField(VM *vm, uint32_t offset, uint32_t size, void *src) {
  uint32_t paddr = *(uint32_t*)((uint8_t*)vm->run + vm->run->io.data_offset);
  if ((paddr + offset) < paddr) return FAIL;
  if (setMem(vm, paddr + offset, size, src) == FAIL) return FAIL;
  return SUCCESS;
}

uint32_t hp_rand(VM *vm) {
  HYPER_RAND randArg;
  int  fd = open("/dev/urandom", O_RDONLY);
  if (fd < 0) printError("hp_rand::open failed");
  if (read(fd, &randArg.rand, sizeof(uint64_t)) != sizeof(uint64_t)) printError("hp_rand::read failed");
  close(fd);
  if (setHpArgField(vm, offsetof(HYPER_RAND, rand), sizeof(uint64_t), &randArg.rand) == FAIL) return HP_FAIL;
  return HP_SUCCESS;
}

uint32_t hp_time(VM *vm) {
  HYPER_TIME timeArg;
  timeArg.timestamp = time(NULL);
  if (setHpArgField(vm, offsetof(HYPER_TIME, timestamp), sizeof(uint64_t), &timeArg.timestamp) == FAIL) return HP_FAIL;
  return HP_SUCCESS;
}

uint32_t hp_read(VM *vm) {
  HYPER_READ readArg;
  char buf[PAGE_SIZE];
  if (getHpArg(vm, sizeof(HYPER_READ), &readArg) == FAIL) return HP_FAIL;
  if (readArg.fd != STDIN_FILENO) return HP_FAIL;
  if (readArg.size > PAGE_SIZE) return HP_FAIL;
  for (uint64_t cursor = 0, readSize = 0; cursor < readArg.size; cursor += readSize) {
    if ((readSize = read(readArg.fd, &buf[cursor], readArg.size - cursor)) <= 0) return HP_FAIL;
  }
  if (setMem(vm, readArg.paddr, readArg.size, buf) == FAIL) return HP_FAIL;
  return HP_SUCCESS;
}

uint32_t hp_write(VM *vm) {
  HYPER_WRITE writeArg;
  char buf[PAGE_SIZE];
  if (getHpArg(vm, sizeof(HYPER_WRITE), &writeArg) == FAIL) return HP_FAIL;
  if (writeArg.fd != STDOUT_FILENO) return HP_FAIL;
  if (writeArg.size > PAGE_SIZE) return HP_FAIL;
  if (getMem(vm, writeArg.paddr, writeArg.size, buf) == FAIL) return HP_FAIL;
  if (write(writeArg.fd, buf, writeArg.size) != writeArg.size) return HP_FAIL;
  return HP_SUCCESS;
}

void __attribute__((noreturn)) hp_exit(VM *vm) {
  _exit(0);
}

uint32_t hp_digestGenerate(VM *vm) {
  HYPER_DIGEST digestArg;
  if (getHpArg(vm, sizeof(HYPER_DIGEST), &digestArg) == FAIL) return HP_FAIL;
  if (digestArg.dataLen > DIGEST_PAYLOAD_SIZE_MAX) return HP_FAIL;
  SHA256(digestArg.data, digestArg.dataLen, digestArg.digest);
  if (setHpArgField(vm, offsetof(HYPER_DIGEST, digest), DIGEST_SIZE, digestArg.digest) == FAIL) return HP_FAIL;
  return HP_SUCCESS;
}

uint32_t hp_signatureValidate(VM *vm) {
  HYPER_SIGNATURE signatureArg;
  OSSL_PARAM_BLD *paramBld = NULL;
  OSSL_PARAM *param = NULL;
  BIGNUM *n = NULL, *e = NULL;
  EVP_PKEY_CTX *ctx = NULL;
  EVP_PKEY *pubkey = NULL;
  uint32_t res = HP_FAIL;
  if (getHpArg(vm, sizeof(HYPER_SIGNATURE), &signatureArg) == FAIL) goto DONE;
  if ((n = BN_new()) == NULL) goto DONE;
  if ((e = BN_new()) == NULL) goto DONE;
  BN_lebin2bn(signatureArg.pubkeyN, SIGNATURE_SIZE, n);
  BN_lebin2bn(signatureArg.pubkeyE, SIGNATURE_SIZE, e);
  if ((paramBld = OSSL_PARAM_BLD_new()) == NULL) goto DONE;
  if (OSSL_PARAM_BLD_push_BN(paramBld, "n", n) <= 0) goto DONE;
  if (OSSL_PARAM_BLD_push_BN(paramBld, "e", e) <= 0) goto DONE;
  if ((param = OSSL_PARAM_BLD_to_param(paramBld)) == NULL) goto DONE;
  if ((ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL)) == NULL) goto DONE;
  if (EVP_PKEY_fromdata_init(ctx) <= 0) goto DONE;
  if (EVP_PKEY_fromdata(ctx, &pubkey, EVP_PKEY_PUBLIC_KEY, param) <= 0) goto DONE;
  EVP_PKEY_CTX_free(ctx);
  if ((ctx = EVP_PKEY_CTX_new(pubkey, NULL)) == NULL) goto DONE;
  if (EVP_PKEY_verify_init(ctx) <= 0) goto DONE;
  if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_PADDING) <= 0) goto DONE;
  if (EVP_PKEY_CTX_set_signature_md(ctx, EVP_sha256()) <= 0) goto DONE;
  if (EVP_PKEY_verify(ctx, signatureArg.signature, SIGNATURE_SIZE, signatureArg.digest, DIGEST_SIZE) <= 0) goto DONE;
  res = HP_SUCCESS;
DONE:
  if (n != NULL) {
    BN_free(n);
  }
  if (e != NULL) {
    BN_free(e);
  }
  if (paramBld != NULL) {
    OSSL_PARAM_BLD_free(paramBld);
  }
  if (param != NULL) {
    OSSL_PARAM_free(param);
  }
  if (ctx != NULL) {
    EVP_PKEY_CTX_free(ctx);
  }
  if (pubkey != NULL) {
    EVP_PKEY_free(pubkey);
  }
  return res;
}

uint32_t hp_appletRegisterValidate(VM *vm) {
  HYPER_APPLET registerArg;
  DV_APPLET_REGISTER_RES res;
  if (getHpArg(vm, sizeof(HYPER_APPLET), &registerArg) == FAIL) return HP_FAIL;
  if (registerArg.codeLen == 0 || registerArg.codeLen > APPLET_SIZE_MAX) return HP_FAIL;
  dv_sendMsg(DV_APPLET_REGISTER_MSG, (uint8_t*)&registerArg, sizeof(HYPER_APPLET));
  dv_recvMsg(DV_APPLET_REGISTER_MSG, (uint8_t*)&res, sizeof(DV_APPLET_REGISTER_RES));
  if (res == DV_FAIL) return HP_FAIL;
  return HP_SUCCESS;
}

uint32_t hp_appletInvoke(VM *vm) {
  HYPER_APPLET_INVOKE invokeArg;
  DV_APPLET_INVOKE_RES res;
  if (getHpArg(vm, sizeof(HYPER_APPLET_INVOKE), &invokeArg) == FAIL) return HP_FAIL;
  if (invokeArg.dataLen > APPLET_ARG_SIZE_MAX) return HP_FAIL;
  dv_sendMsg(DV_APPLET_INVOKE_MSG, (uint8_t*)&invokeArg, sizeof(HYPER_APPLET_INVOKE));
  dv_recvMsg(DV_APPLET_INVOKE_MSG, (uint8_t*)&res, sizeof(DV_APPLET_INVOKE_RES));
  if (res == DV_FAIL) return HP_APPLET_PROCESSOR_REJECT;
  if (res == DV_BUSY) return HP_APPLET_PROCESSOR_BUSY;
  return HP_SUCCESS;
}

uint32_t hp_appletResume(VM *vm) {
  HYPER_APPLET_RESUME resumeArg;
  DV_APPLET_RESUME_RES res;
  if (getHpArg(vm, sizeof(HYPER_APPLET_RESUME), &resumeArg) == FAIL) return HP_FAIL;
  dv_sendMsg(DV_APPLET_RESUME_MSG, (uint8_t*)&resumeArg, sizeof(HYPER_APPLET_RESUME));
  dv_recvMsg(DV_APPLET_RESUME_MSG, (uint8_t*)&res, sizeof(DV_APPLET_RESUME_RES));
  if (res == DV_FAIL) return HP_APPLET_PROCESSOR_REJECT;
  if (res == DV_BUSY) return HP_APPLET_PROCESSOR_BUSY;
  return HP_SUCCESS;
}

void printFlag(char *fname) {
  int fsize, fd = open(fname, O_RDONLY);
  char buf[FLAG_SIZE_MAX];
  if (fd < 0) printError("printFlag::open failed");
  if ((fsize = read(fd, buf, FLAG_SIZE_MAX - 1)) <= 0) printError("hp_appletspaceFlag::read failed");
  buf[fsize] = '\x00';
  puts(buf);
  close(fd);
  return;
}

uint32_t hp_appletspaceFlag(VM *vm) {
  printFlag(APPLETSPACE_FLAG_FNAME);
  return HP_SUCCESS;
}

uint32_t hp_userspaceFlag(VM *vm) {
  printFlag(USERSPACE_FLAG_FNAME);
  return HP_SUCCESS;
}

uint32_t hp_kernelspaceFlag(VM *vm) {
  printFlag(KERNELSPACE_FLAG_FNAME);
  return HP_SUCCESS;
}
