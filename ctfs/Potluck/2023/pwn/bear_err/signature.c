#include "signature.h"
#include <openssl/pem.h>
#include <openssl/err.h>

RSA* createPrivateRSA(char* key) {
  RSA *rsa = NULL;
  const char* c_string = key;
  BIO * keybio = BIO_new_mem_buf((void*)c_string, -1);
  if (keybio==NULL) {
    printf("Couldn't create buffer\n");
    return 0;
  }
  rsa = PEM_read_bio_RSAPrivateKey(keybio, &rsa, NULL, NULL);
  if(!rsa)
    ERR_print_errors_fp (stderr);
  return rsa;
}

bool RSASign( RSA* rsa, 
              const unsigned char* Msg, 
              size_t MsgLen,
              unsigned char** EncMsg, 
              size_t* MsgLenEnc) {
  EVP_MD_CTX* m_RSASignCtx = EVP_MD_CTX_create();
  EVP_PKEY* priKey  = EVP_PKEY_new();
  EVP_PKEY_assign_RSA(priKey, rsa);
  if (EVP_DigestSignInit(m_RSASignCtx,NULL, EVP_sha512_256(), NULL,priKey)<=0) {
      return false;
  }
  if (EVP_SignUpdate(m_RSASignCtx, Msg, MsgLen) <= 0) {
      return false;
  }
  if (EVP_DigestSignFinal(m_RSASignCtx, NULL, MsgLenEnc) <=0) {
      return false;
  }
  *EncMsg = (unsigned char*)malloc(*MsgLenEnc);
  if (EVP_DigestSignFinal(m_RSASignCtx, *EncMsg, MsgLenEnc) <= 0) {
      return false;
  }
  EVP_MD_CTX_destroy(m_RSASignCtx);
  return true;
}

RSA* createPublicRSA(char* key) {
  RSA *rsa = NULL;
  BIO *keybio;
  const char* c_string = key;
  keybio = BIO_new_mem_buf((void*)c_string, -1);
  if (keybio==NULL) {
    printf("Couldn't create buffer\n");
    return 0;
  }
  rsa = PEM_read_bio_RSA_PUBKEY(keybio, &rsa,NULL, NULL);
  if(!rsa)
    ERR_print_errors_fp (stderr);
  return rsa;
}

bool RSAVerifySignature( RSA* rsa, 
                         unsigned char* MsgHash, 
                         size_t MsgHashLen, 
                         const char* Msg, 
                         size_t MsgLen, 
                         bool* Authentic) {
  *Authentic = false;
  EVP_PKEY* pubKey  = EVP_PKEY_new();
  EVP_PKEY_assign_RSA(pubKey, rsa);
  EVP_MD_CTX* m_RSAVerifyCtx = EVP_MD_CTX_create();
  if (EVP_DigestVerifyInit(m_RSAVerifyCtx,NULL, EVP_sha512_256(),NULL,pubKey)<=0) {
    ERR_print_errors_fp (stderr);
    return false;
  }
  if (EVP_VerifyUpdate(m_RSAVerifyCtx, Msg, MsgLen) <= 0) {
    printf("Invalid signature\n");
    ERR_print_errors_fp (stderr);
    return false;
  }
  int AuthStatus = EVP_DigestVerifyFinal(m_RSAVerifyCtx, MsgHash, MsgHashLen);
  if (AuthStatus==1) {
    *Authentic = true;
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return true;
  } else if(AuthStatus==0){
    *Authentic = false;
    printf("Invalid signature\n");
    ERR_print_errors_fp (stderr);
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return true;
  } else{
    *Authentic = false;
    printf("Invalid signature\n");
    ERR_print_errors_fp (stderr);
    EVP_MD_CTX_destroy(m_RSAVerifyCtx);
    return false;
  }
}