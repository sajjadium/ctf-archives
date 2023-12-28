#include <openssl/rsa.h>
#include <openssl/conf_api.h>
#include <openssl/evp.h>
#include <stdbool.h>

RSA* createPrivateRSA(char* key);
bool RSASign( RSA* rsa, 
              const unsigned char* Msg, 
              size_t MsgLen,
              unsigned char** EncMsg, 
              size_t* MsgLenEnc);
RSA* createPublicRSA(char* key);
bool RSAVerifySignature(RSA* rsa, 
                         unsigned char* MsgHash, 
                         size_t MsgHashLen, 
                         const char* Msg, 
                         size_t MsgLen, 
                         bool* Authentic);