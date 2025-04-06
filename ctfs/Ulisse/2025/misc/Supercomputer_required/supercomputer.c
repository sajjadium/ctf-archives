#include <arpa/inet.h>
#include <ctype.h>
#include <openssl/rand.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define NAME_SIZE 16384 
#define DIM_BUFF 2
#define CHALLENGE_SIZE 32
#define DIFFICULTY 24

#ifndef FLAG
#define FLAG "UlisseCTF{REDACTED}"
#endif

void reap_zombies(int sig) {
  while (waitpid(-1, NULL, WNOHANG) > 0)
    ;
}

long get_time_ms() {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (ts.tv_sec * 1000L) + (ts.tv_nsec / 1000000L);
}

void to_hex(const unsigned char *data, int length, char *hex_output) {
  for (int i = 0; i < length; i++) {
    sprintf(hex_output + (i * 2), "%02x", data[i]);
  }
}

int from_hex(const char *hex, int length, unsigned char *output) {
  for (size_t i = 0; i < length; i++) {
    if (!isxdigit(hex[i * 2]) || !isxdigit(hex[i * 2 + 1])) {
      return -1;
    }
    if (sscanf(hex + (i * 2), "%2hhx", &output[i]) != 1) {
      return -1;
    }
  }
  return 0;
}

void generate_challenge(unsigned char *challenge) {
  if (RAND_bytes(challenge, CHALLENGE_SIZE) != 1) {
    perror("RAND bytes");
    exit(EXIT_FAILURE);
  }
}

int validate_pow(const unsigned char *challenge, const unsigned char *nonce) {
  unsigned char hash[SHA256_DIGEST_LENGTH];
  unsigned char data[CHALLENGE_SIZE + CHALLENGE_SIZE];
  memcpy(data, challenge, CHALLENGE_SIZE);
  memcpy(data + CHALLENGE_SIZE, nonce, CHALLENGE_SIZE);
  SHA256(data, CHALLENGE_SIZE * 2, hash);
  for (int i = 0; i < DIFFICULTY; i++) {
    if ((hash[i / 8] & (1 << (7 - (i % 8)))) != 0) {
      return 0;
    }
  }
  return 1;
}

int main(int argc, char *argv[]) {
  int sd, cd;
  char buff[DIM_BUFF];
  struct sockaddr_in client_addr;
  int client_len = sizeof(client_addr);

  if (argc != 2) {
    printf("Error:%s serverPort\n", argv[0]);
    exit(1);
  }
  printf("Server started\n");
  sd = socket(AF_INET, SOCK_STREAM, 0);
  struct sockaddr_in own_addr;
  memset(&own_addr, 0, sizeof(own_addr));
  own_addr.sin_family = AF_INET;
  own_addr.sin_addr.s_addr = INADDR_ANY;
  own_addr.sin_port = htons(atoi(argv[1]));

  int opt = 1;
  if (setsockopt(sd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt)) < 0) {
    perror("setsockopt(SO_REUSEPORT) failed");
    close(sd);
    exit(1);
  }
  if (bind(sd, (struct sockaddr *)&own_addr, sizeof(own_addr)) < 0) {
    perror("bind failed");
    exit(1);
  }
  printf("binded on port %d\n", ntohs(own_addr.sin_port));
  if (listen(sd, 5) < 0) {
    perror("listen failed");
    exit(1);
  }
  printf("listening\n");

  struct sigaction sa;
  sa.sa_handler = reap_zombies;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = SA_RESTART;
  sigaction(SIGCHLD, &sa, NULL);

  for (;;) {
    cd = accept(sd, (struct sockaddr *)&client_addr, &client_len);

    int sndbuf= 4096;
    socklen_t optlen = sizeof(sndbuf);
    if( setsockopt(cd, SOL_SOCKET, SO_SNDBUF, &sndbuf, optlen) == -1){
      close(cd);
      continue;
    }

    if (fork() == 0) {
      close(sd);

      char * menu="insert your username:\n";
      if(send(cd,menu,strlen(menu),0) <= 0){
        close(cd);
	exit(1);
      }
      char * name= malloc(NAME_SIZE);
      int ind=0;
      char charbuf;
      while(ind<NAME_SIZE){
        if(recv(cd,&charbuf,1,0)<1){
          close(cd);
	  exit(1);
        }
	if(charbuf=='\n'){
          break;
	}
	name[ind]=charbuf;
	ind++;
      }
      if(ind==NAME_SIZE){
        close(cd);
	exit(1);
      }
      name[ind]='\0';

      bool certified_supercomputer_owner = false;
      while (1) {
        char *menu =
            " 0) exit\n 1) check current status\n 2) start supercomputer "
            "ownership verification process\n 3) get flag\n=>";
        if (send(cd, menu, strlen(menu), 0) <= 0)
          break;
        if (recv(cd, &buff, DIM_BUFF, 0) < DIM_BUFF)
          break;
        int choice = atoi(buff);
        if (choice == 1) {
          if (certified_supercomputer_owner) {
            char *response = "you are a sigma certified supercomputer owner\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          } else {
            char *response = "you are a pleeb supercomputer-less commoner\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          }
        } else if (choice == 2) {
          unsigned char challenge[CHALLENGE_SIZE];
          generate_challenge(challenge);
          char challenge_hex[2 * CHALLENGE_SIZE];
          to_hex(challenge, CHALLENGE_SIZE, challenge_hex);
          char *response = "solve this proof of work: ";
          if (send(cd, response, strlen(response), 0) <= 0)
            break;
          if (send(cd, challenge_hex, 2 * CHALLENGE_SIZE, 0) <= 0)
            break;
          response = " in less than 0.01 seconds to prove you have a "
                     "supercomputer and elevate the status of user ";
          if (send(cd, response, strlen(response), 0) <= 0)
            break;
	  if (send(cd,name,strlen(name),0) <= 0)
            break;
          response = ":\n";
          if (send(cd, response, strlen(response), 0) <= 0)
            break;

          long start_time = get_time_ms();

          char nonce_hex[2 * CHALLENGE_SIZE + 1];
          if (recv(cd, nonce_hex, 2 * CHALLENGE_SIZE + 1, 0) < 0)
            break;

          long end_time = get_time_ms();
          if (end_time - start_time > 10) {
            response = "too slow\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
            continue;
          }

          unsigned char nonce[CHALLENGE_SIZE];
          if (from_hex(nonce_hex, CHALLENGE_SIZE, nonce) == -1) {
            response = "invalid hex\n";
            continue;
          }
          if (validate_pow(challenge, nonce) == 1) {
            certified_supercomputer_owner = true;
            response = "welcome to the club\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          } else {
            response = "incorrect proof of work\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          }

        } else if (choice == 3) {
          if (certified_supercomputer_owner) {
            char *response = "here's your flag: "  FLAG  "\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          } else {
            char *response =
                "the flag is for certified supercomputer owners only\n";
            if (send(cd, response, strlen(response), 0) <= 0)
              break;
          }
        } else {
          break;
        }
      }
      close(cd);
      exit(0);
    } else {
      close(cd);
    }
  }
}

