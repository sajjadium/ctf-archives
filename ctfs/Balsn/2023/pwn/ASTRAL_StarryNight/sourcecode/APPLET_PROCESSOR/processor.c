#include "processor.h"

void initSnapshot(SNAPSHOT *snapshot) {
  for (uint64_t i = 0; i < APPLET_TASK_CNT_MAX; i++) {
    snapshot[i].task = APPLET_TASK_NIL;
  }
  return;
}

void getDigest(uint8_t *in, uint64_t size, uint8_t *out) {
  SHA256(in, size, out);
  return;
}

uint64_t validateSignature(uint8_t *digest, uint8_t *signature) {
  OSSL_PARAM_BLD *paramBld = NULL;
  OSSL_PARAM *param = NULL;
  BIGNUM *n = NULL, *e = NULL;
  EVP_PKEY_CTX *ctx = NULL;
  EVP_PKEY *pubkey = NULL;
  uint64_t res = FAIL;
  if ((n = BN_new()) == NULL) goto DONE;
  if ((e = BN_new()) == NULL) goto DONE;
  BN_lebin2bn(AUTHORITY_KEY_N, SIGNATURE_SIZE, n);
  BN_lebin2bn(AUTHORITY_KEY_E, SIGNATURE_SIZE, e);
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
  if (EVP_PKEY_verify(ctx, signature, SIGNATURE_SIZE, digest, DIGEST_SIZE) <= 0) goto DONE;
  res = SUCCESS;
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

uint64_t appletCheckSignature(DEVICE_APPLET *applet) {
  uint8_t digest[DIGEST_SIZE];
  if (applet->codeLen == 0 || applet->codeLen > APPLET_SIZE_MAX) return FAIL;
  getDigest(applet->code, applet->codeLen, digest);
  if (validateSignature(digest, applet->authoritySignature) == FAIL) return FAIL;
  return SUCCESS;
}

uint64_t appletCheckSnapshot(DEVICE_APPLET_RESUME *resume, SNAPSHOT *snapshot, bool clear) {
  uint8_t digest[DIGEST_SIZE];
  getDigest((uint8_t*)&resume->context, sizeof(DEVICE_APPLET_CONTEXT), digest);
  for (uint64_t i = 0; i < APPLET_TASK_CNT_MAX; i++) {
    if (snapshot[i].task == resume->context.task) {
      if (clear) {
        snapshot[i].task = APPLET_TASK_NIL;
      }
      if (!memcmp(snapshot[i].checkpointDigest, digest, DIGEST_SIZE)) {
        return SUCCESS;
      } else {
        return FAIL;
      } 
    }
  }
  return FAIL;
}

uint64_t findSpareSnapshotSlot(SNAPSHOT *snapshot, uint64_t *spareSlot) {
  for (uint64_t i = 0; i < APPLET_TASK_CNT_MAX; i++) {
    if (snapshot[i].task == APPLET_TASK_NIL) {
      *spareSlot = i;
      return SUCCESS;
    }
  }
  return FAIL;
}

void processMsg(SNAPSHOT *snapshot) {
  uint8_t buf[DV_MSG_DATA_SIZE_MAX];
  switch (dv_recvMsg(buf, false)) {
    case DV_NO_MSG:
      break;
    case DV_APPLET_REGISTER_MSG:
      DEVICE_APPLET *registerReq = (DEVICE_APPLET*)buf;
      DV_APPLET_REGISTER_RES registerRes;
      if (appletCheckSignature(registerReq) == SUCCESS) {
        registerRes = DV_SUCCESS;
      } else {
        registerRes = DV_FAIL;
      }
      dv_sendMsg(DV_APPLET_REGISTER_MSG, (uint8_t*)&registerRes, sizeof(DV_APPLET_REGISTER_RES));
      break;
    case DV_APPLET_INVOKE_MSG:
      DEVICE_APPLET_INVOKE *invokeReq = (DEVICE_APPLET_INVOKE*)buf;
      DV_APPLET_INVOKE_RES invokeRes;
      if (appletCheckSignature(&invokeReq->applet) == SUCCESS) {
        invokeRes = DV_BUSY;
      } else {
        invokeRes = DV_FAIL;
      }
      if (invokeReq->dataLen > APPLET_ARG_SIZE_MAX) {
        invokeRes = DV_FAIL;
      }
      dv_sendMsg(DV_APPLET_INVOKE_MSG, (uint8_t*)&invokeRes, sizeof(DV_APPLET_INVOKE_RES));
      break;
    case DV_APPLET_RESUME_MSG:
      DEVICE_APPLET_RESUME *resumeReq = (DEVICE_APPLET_RESUME*)buf;
      DV_APPLET_RESUME_RES resumeRes;
      uint64_t snapshotIdx;
      if (appletCheckSnapshot(resumeReq, snapshot, false) == SUCCESS) {
        resumeRes = DV_BUSY;
      } else {
        resumeRes = DV_FAIL;
      }
      if (resumeReq->resLen > APPLET_RES_SIZE_MAX) {
        resumeRes = DV_FAIL;
      }
      dv_sendMsg(DV_APPLET_RESUME_MSG, (uint8_t*)&resumeRes, sizeof(DV_APPLET_RESUME_RES));
      break;
    default:
      printError("unknown msg");
  }
  return;
}

void handleAppletExit(APPLET_CONTEXT *context, APPLET_TASK_ID task, SNAPSHOT *snapshot) {
  uint64_t spareSlot;
  if (context->exitReason == EXIT_INVOKE && findSpareSnapshotSlot(snapshot, &spareSlot) == SUCCESS) {
    DEVICE_APPLET_CONTEXT appletContext;
    appletContext.task = task;
    memcpy(appletContext.regs, context->regs, sizeof(uint64_t) * APPLET_REG_CNT);
    memcpy(appletContext.memory, context->memory, APPLET_CONTEXT_MEMORY_SIZE);
    getDigest((uint8_t*)&appletContext, sizeof(DEVICE_APPLET_CONTEXT), snapshot[spareSlot].checkpointDigest);
    snapshot[spareSlot].task = task;
    dv_sendInterrupt(DV_APPLET_INVOKE_INTERRUPT, (uint8_t*)&appletContext, sizeof(DEVICE_APPLET_CONTEXT));
  } else {
    DEVICE_APPLET_RES appletRes;
    uint64_t offset;
    memset(appletRes.res, '\0', APPLET_RES_SIZE_MAX);
    appletRes.task = task;
    if (translateMem(context->regs[APPLET_RES_ADDR], context->regs[APPLET_RES_LEN], &offset) == FAIL) {
      appletRes.resLen = sizeof(uint64_t);
      *((uint64_t*)appletRes.res) = APPLET_FAIL;
    } else {
      appletRes.resLen = context->regs[APPLET_RES_LEN];
      memcpy(appletRes.res, &context->memory[offset], appletRes.resLen);
    }
    translateMem(APPLET_STORAGE_SEG_ADDR, APPLET_STORAGE_SIZE, &offset);
    memcpy(appletRes.storage, &context->memory[offset], APPLET_STORAGE_SIZE);
    dv_sendInterrupt(DV_APPLET_RES_INTERRUPT, (uint8_t*)&appletRes, sizeof(DEVICE_APPLET_RES));
  }
  return;
}

void invokeApplet(APPLET_CONTEXT *context, DEVICE_APPLET_INVOKE *invoke, SNAPSHOT *snapshot) {
  resetAppletContext(context);
  setMem(context, APPLET_CODE_SEG_ADDR, invoke->applet.code, invoke->applet.codeLen);
  setMem(context, APPLET_INPUT_SEG_ADDR, invoke->data, invoke->dataLen);
  setMem(context, APPLET_STORAGE_SEG_ADDR, invoke->storage, APPLET_STORAGE_SIZE);
  context->regs[APPLET_CALLER] = invoke->caller;
  context->regs[APPLET_INP_LEN] = invoke->dataLen;
  runApplet(context, snapshot, processMsg);
  handleAppletExit(context, invoke->task, snapshot);
  return;
}

void resumeApplet(APPLET_CONTEXT *context, DEVICE_APPLET_RESUME *resume, SNAPSHOT *snapshot) {
  resetAppletContext(context);
  memcpy(context->regs, resume->context.regs, sizeof(uint64_t) * APPLET_REG_CNT);
  memcpy(context->memory, resume->context.memory, APPLET_CONTEXT_MEMORY_SIZE);
  if (setMem(context, context->regs[APPLET_INVOKE_RES_ADDR], resume->res, resume->resLen) == FAIL) {
    context->exitReason = EXIT_DONE;
    handleAppletExit(context, resume->context.task, snapshot);
  } else {
    runApplet(context, snapshot, processMsg);
    handleAppletExit(context, resume->context.task, snapshot);
  }
  return;
}

int main() {
  SNAPSHOT snapshot[APPLET_TASK_CNT_MAX];
  APPLET_CONTEXT context;
  uint8_t buf[DV_MSG_DATA_SIZE_MAX];
  applySeccomp();
  initSnapshot(snapshot);
  initAppletContext(&context);
  initDevice();
  while (true) {
    switch (dv_recvMsg(buf, true)) {
      case DV_NO_MSG:
        break;
      case DV_APPLET_REGISTER_MSG:
        DEVICE_APPLET *registerReq = (DEVICE_APPLET*)buf;
        DV_APPLET_REGISTER_RES registerRes;
        if (appletCheckSignature(registerReq) == SUCCESS) {
          registerRes = DV_SUCCESS;
        } else {
          registerRes = DV_FAIL;
        }
        dv_sendMsg(DV_APPLET_REGISTER_MSG, (uint8_t*)&registerRes, sizeof(DV_APPLET_REGISTER_RES));
        break;
      case DV_APPLET_INVOKE_MSG:
        DEVICE_APPLET_INVOKE *invokeReq = (DEVICE_APPLET_INVOKE*)buf;
        DV_APPLET_INVOKE_RES invokeRes;
        if (appletCheckSignature(&invokeReq->applet) == SUCCESS) {
          invokeRes = DV_SUCCESS;
        } else {
          invokeRes = DV_FAIL;
        }
        if (invokeReq->dataLen > APPLET_ARG_SIZE_MAX) {
          invokeRes = DV_FAIL;
        }
        dv_sendMsg(DV_APPLET_INVOKE_MSG, (uint8_t*)&invokeRes, sizeof(DV_APPLET_INVOKE_RES));
        if (invokeRes == DV_SUCCESS) {
          invokeApplet(&context, invokeReq, snapshot);
        }
        break;
      case DV_APPLET_RESUME_MSG:
        DEVICE_APPLET_RESUME *resumeReq = (DEVICE_APPLET_RESUME*)buf;
        DV_APPLET_RESUME_RES resumeRes;
        uint64_t snapshotIdx;
        if (appletCheckSnapshot(resumeReq, snapshot, true) == SUCCESS) {
          resumeRes = DV_SUCCESS;
        } else {
          resumeRes = DV_FAIL;
        }
        if (resumeReq->resLen > APPLET_RES_SIZE_MAX) {
          resumeRes = DV_FAIL;
        }
        dv_sendMsg(DV_APPLET_RESUME_MSG, (uint8_t*)&resumeRes, sizeof(DV_APPLET_RESUME_RES));
        if (resumeRes == DV_SUCCESS) {
          resumeApplet(&context, resumeReq, snapshot);
        }
        break;
      default:
        printError("unknown msg");
    }
  }
  return 0;
}
