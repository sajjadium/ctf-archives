#include <iostream>
#include <memory>
#include <fstream>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>
#include <unistd.h>

class SecretServiceImpl {

  public:

    SecretServiceImpl() {
      std::cin.rdbuf()->pubsetbuf(0, 0);
      std::cin.setf(std::ios::unitbuf);
      std::cout.rdbuf()->pubsetbuf(0,0);
      std::cout.setf(std::ios::unitbuf);

      std::cout << "Username: ";
      std::cin.read(username, sizeof(username));
      std::cout << "Password: ";
      std::cin.read(password, sizeof(password));

      std::ifstream urand("/dev/urandom",std::ifstream::in);
      urand.read((char*)Key,0x10);
      urand.read((char*)IV, 0x10);
      urand.close();

      secret = new char[0x200];
      memset(secret, 0, 0x200);
      bzero(fence, sizeof(fence));
    }

    void edit_password() {
      std::cout << "Password: ";
      read(0, password, strlen(password));
    }

    void edit_username() {
      std::cout << "Username: ";
      read(0, username, strlen(username));
    }

    void view_secret() {
      std::cout << "Secret = ";
      write(1, secret, 0x20);
      std::cout << std::endl;
    }

    void encrypt_secret() {
      EVP_CIPHER_CTX *ctx;
      int len;
      if(!(ctx = EVP_CIPHER_CTX_new()))
          error("Encrypt");
      if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL,(unsigned char*)Key,(unsigned char*)IV))
          error("Encrypt");
      if(1 != EVP_EncryptUpdate(ctx, (unsigned char*)secret, &len, (unsigned char*)username, 0x10))
          error("Encrypt");
      if(1 != EVP_EncryptFinal_ex(ctx, (unsigned char*)secret + len, &len))
          error("Encrypt");
      EVP_CIPHER_CTX_free(ctx);      
    }

    void error(std::string errstring) {
      std::cout << errstring << std::endl;
      std::exit(-1);
    }

  private:
    char username[0x10];
    char password[0x10];
    char Key[0x10];
    char IV[0x10];
    char* secret;
    char fence[0x10];
};

int main() {
  SecretServiceImpl service;
  uint32_t cmd;
  while(true) {
    std::cout << ">> ";
    std::cin >> cmd;
    switch(cmd) {
      case 0:
        service.edit_password();
        break;
      case 1:
        service.edit_username();
        break;
      case 2:
        service.encrypt_secret();
        break;
      case 3:
        service.view_secret();
        break;
      default:
        break;
    }
  }
}
