//gcc main.c -o main

#include <stdint.h>
#include <sys/socket.h>
#include <stddef.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define MAX_HEADER_LEN 36

enum pkt_type_t {
  PKT_HELO,
  PKT_SIGNUP,
  PKT_LOGOUT,
  PKT_ADD,
  PKT_GET,
  PKT_DEL,
  PKT_BUG
};

typedef struct cl_srv_res_t {
  uint8_t status;
  uint8_t *res;
} cl_srv_res_t;


typedef struct __attribute__((__packed__))  pkt_inst_helo_t {
  uint8_t identifier;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_helo_t;

typedef struct __attribute__((__packed__)) pkt_inst_signup_t {
  uint8_t identifier;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_signup_t;

typedef struct __attribute__((__packed__)) pkt_inst_bye_t {
  uint8_t identifier;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_bye_t;

typedef struct __attribute__((__packed__)) pkt_inst_add_t {
  uint8_t identifier;
  long index;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_add_t;

typedef struct __attribute__((__packed__)) pkt_inst_get_t {
  uint8_t identifier;
  long index;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_get_t;

typedef struct __attribute__((__packed__)) pkt_inst_del_t {
  uint8_t identifier;
  long index;
  uint8_t has_body;
  uint16_t len;
} pkt_inst_del_t;

typedef struct __attribute__((__packed__)) pkt_inst_bug_t {
  uint8_t identifier;
  char title[32];
  uint8_t has_body;
  uint16_t len;
} pkt_inst_bug_t;

const uint8_t pkt_hdr_len[] = {
  sizeof(pkt_inst_helo_t),
  sizeof(pkt_inst_signup_t),
  sizeof(pkt_inst_bye_t),
  sizeof(pkt_inst_add_t),
  sizeof(pkt_inst_get_t),
  sizeof(pkt_inst_del_t),
  sizeof(pkt_inst_bug_t)
};

int cl_logged_in = 0;

void hex_dump(size_t len, uint8_t * buf){
  while(len--){
    printf("%02x", *buf++);
  }
  puts("");
}

long cl_get_num(){
  char buf[40];
  fgets(buf, 40, stdin);
  buf[39] = 0;
  return strtol(buf, 0, 10);
}

void cl_read_n(int fd, uint8_t *buf, uint16_t n){
  int num_rcv = 0;
  while(n){
    num_rcv = read(fd, buf, n);
    if(num_rcv <= 0){
      printf("[!] Connection closed unexpectedly.\n");
      exit(1);
    }
    n -= num_rcv;
  }
}

void cl_free_res(cl_srv_res_t* res){
  free(res->res);
  free(res);
}

cl_srv_res_t *cl_await_res(int fd){
  uint8_t buf[2];
  // sleep(1); //how to fix buffering 101
  cl_srv_res_t *srv_res = malloc(sizeof(cl_srv_res_t));
  if(!srv_res){
    printf("[!] Could  not allocate response struct.\n");
  }
  cl_read_n(fd, buf, 1);
  // printf("cl: got packet\n---\nstatus %d\n", buf[0]);
  // printf("\n");
  srv_res->status = buf[0];
  cl_read_n(fd, buf, 2);
  // printf("response len %d\n", *((uint16_t *) buf));
  uint8_t *res = malloc(*((uint16_t *) buf));
  if(!res){
    printf("[!] Could not allocate response buffer.\n");
    exit(1);
  }
  cl_read_n(fd, res, *((uint16_t *) buf));
  srv_res->res = res;
  if(srv_res->status == 1){
    printf("[!] Server died:\n  -> ");
    puts((char *)srv_res->res);
    exit(1);
  }
  return srv_res;
}

void cl_send_pkt(int sockfd, uint8_t* packet, char *body, uint16_t body_len){
  uint8_t hdr_len = pkt_hdr_len[packet[0]];
  // printf("\ncl sending packet: \n---\n");
  // printf("cl hdr len %d\n", hdr_len);
  uint8_t has_body = packet[hdr_len - 3];
  // printf("cl body len %d\n", body_len);
  if(write(sockfd, packet, hdr_len) < 0) {
    printf("[!] Connection closed unexpectedly.\n");
    exit(1);
  }  
  if (has_body){
    //not checking if body pointer is valid because passing it
    //does not necessarily imply wanting it to be sent
    if (body_len && !*((uint16_t *) &packet[hdr_len - 2])){
      *((uint16_t *) &packet[hdr_len - 2]) = body_len;
    }
    if(write(sockfd, body, body_len) < 0) {
      printf("[!] Connection closed unexpectedly.\n");
      exit(1);
    }
  }
}

void hello(int fd){
  pkt_inst_helo_t header = {
    PKT_HELO,
    1
  };
  char body_buf[128];
  puts("Enter your name: ");
  fgets(body_buf, 128, stdin);
  body_buf[strcspn(body_buf, "\n")] = 0;
  uint16_t body_len = strlen(body_buf);
  header.len = body_len;
  cl_send_pkt(fd, (uint8_t *) &header, body_buf, body_len);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *)res->res);
    cl_free_res(res);
    return;
  }
  cl_logged_in = 1;
  printf("[*] Successfully logged in.\n");
  cl_free_res(res);
}

void signup(int fd){
  pkt_inst_helo_t header = {
    PKT_SIGNUP,
    1
  };
  char body_buf[128];
  puts("Pick name: ");
  fgets(body_buf, 128, stdin);
  body_buf[strcspn(body_buf, "\n")] = 0;
  uint16_t body_len = strlen(body_buf);
  header.len = body_len;
  cl_send_pkt(fd, (uint8_t *) &header, body_buf, body_len);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *)res->res);
    cl_free_res(res);
    return;
  }
  printf("[*] Successfully registered.\n");
  cl_free_res(res);
}

void logout(int fd){
  pkt_inst_bye_t header = {
    PKT_LOGOUT,
    0
  };
  header.len = 0;
  cl_send_pkt(fd, (uint8_t *) &header, 0, 0);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *)res->res);
    cl_free_res(res);
    return;
  }
  cl_logged_in = 0;
  printf("[*] Logged out.\n");
  cl_free_res(res);
}

void add_pw(int fd){
  pkt_inst_add_t header = {
    PKT_ADD
  };
  char body_buf[256];
  puts("Type your password: ");
  fgets(body_buf, 256, stdin);
  body_buf[strcspn(body_buf, "\n")] = 0;
  uint16_t body_len = strlen(body_buf);
  header.len = body_len;
  header.has_body = 1;
  puts("Select a slot: ");
  header.index = cl_get_num();
  cl_send_pkt(fd, (uint8_t *) &header, body_buf, body_len);  
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *) res->res);
    cl_free_res(res);
    return;
  }
  printf("[*] Password added.\n");
  cl_free_res(res);
}
void get_pw(int fd){
  pkt_inst_get_t header = {
    PKT_GET
  };
  puts("Select a slot: ");
  header.index = cl_get_num();
  cl_send_pkt(fd, (uint8_t *) &header, 0, 0);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *) res->res);
    cl_free_res(res);
    return;
  }
  printf("[*] Password: %s\n", res->res);
  cl_free_res(res);
}
void del_pw(int fd){
  pkt_inst_del_t header = {
    PKT_DEL
  };
  puts("Select a slot: ");
  header.index = cl_get_num();
  cl_send_pkt(fd, (uint8_t *) &header, 0, 0);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *) res->res);
    cl_free_res(res);
    return;
  }
  puts("[*] Password deleted.");
  cl_free_res(res);
}
void report(int fd){
  pkt_inst_bug_t header = {
    PKT_BUG
  };
  char body_buf[4096];
  header.has_body = 1;
  puts("Type your bug report: ");
  uint16_t body_len = read(0, body_buf, 4096);
  header.len = body_len;
  puts("Pick a title: ");
  read(0, header.title, 32);
  header.title[strcspn(header.title, "\n")] = 0;
  cl_send_pkt(fd, (uint8_t *) &header, body_buf, body_len);
  cl_srv_res_t *res = cl_await_res(fd);
  if(res->status){
    printf("[!] Server error:\n  -> ");
    puts((char *) res->res);
    cl_free_res(res);
    return;
  }
  puts("[*] Report filed.");
  cl_free_res(res);
}

void cl_login_prompt(){
  printf("What would you like to do?\n\
1) Login\n\
2) Sign Up\n\
3) Quit\n\
> ");
}

void cl_menu_prompt(){
  printf("What would you like to do?\n\
1) Add password\n\
2) Get password\n\
3) Delete password\n\
4) Logout\n\
> ");
}

void client(int fd){
  long choice;
  while(1){
    if(!cl_logged_in){
      cl_login_prompt();
      choice = cl_get_num();
      if(!(choice > 0 && choice < 5)){
        printf("[!] Invalid choice, try again.\n");
        continue;
      }
      switch(choice){
        case 1:
          hello(fd); break;
        case 2:
          signup(fd); break;
        case 3:
          exit(0); break;
        case 4:
          report(fd); break;
      }
      continue;
    }
    cl_menu_prompt();
    choice = cl_get_num();
    if(!(choice > 0 && choice < 5)){
      printf("[!] Invalid choice, try again.\n");
      continue;
    }
    switch(choice){
      case 1:
        add_pw(fd); break;
      case 2:
        get_pw(fd); break;
      case 3:
        del_pw(fd); break;
      case 4:
        logout(fd); break;
    }
  }
}

#define MAX_USERS 20
#define MAX_PASSWORDS 20

typedef struct srv_parse_state_t {
  uint8_t *packet;
  uint16_t i;
  uint8_t identifier;
  uint8_t header_length;
  uint16_t data_length;
  uint8_t header[MAX_HEADER_LEN];
  uint8_t *data;
  int state;
} srv_parse_state_t; 

enum SRV_PARSE_STATE {
  SRV_PARSE_INIT,
  SRV_PARSE_HDR,
  SRV_PARSE_DATA,
  SRV_PARSE_DISPATCH
};

typedef struct srv_pw_t {
  uint64_t len;
  char *password;
} srv_pw_t;

typedef struct srv_user_t {
  char* username;
  uint32_t username_len;
  srv_pw_t passwords[MAX_PASSWORDS];
} srv_user_t;

srv_user_t **srv_users;
srv_user_t *srv_curr_user;

void srv_res(int fd, uint8_t status, uint16_t len, void* body){
  if(write(fd, &status, 1) < 0 || write(fd, &len, 2) < 0 || write(fd, body, len) < 0){
    printf("[!] Connection closed unexpectedly.\n");
    exit(1);
  }
}

void srv_err(int fd, char* body){
  uint16_t len = strlen(body);
  srv_res(fd, 2, len, body);
}

void srv_die(int fd, char* body){
  uint16_t len = strlen(body);
  srv_res(fd, 1, len, body);
}

void srv_handle_helo(int fd, uint8_t* packet, uint16_t packet_len){
  int exists = -1;
  for(int i = 0; i < MAX_USERS; i++){
    if(!srv_users[i]) continue;
    // hex_dump(10, srv_users[i]->username);
    // hex_dump(10, packet);
    if( packet_len != srv_users[i]->username_len ||
    strncmp(
      srv_users[i]->username, 
      (char *) packet,
      packet_len
    )) continue;
    exists = i;
    break;
  }
  if(exists < 0){
    srv_err(fd, "User not found.");
    return;
  }
  srv_curr_user = srv_users[exists];
  srv_res(fd, 0, 0, "");
}

void srv_handle_signup(int fd, uint8_t* packet, uint16_t packet_len){
  int free_space = -1;
  for(int i = 0; i < MAX_USERS; i++){
    if(!srv_users[i]) {
      if(free_space == -1){
        free_space = i;
      }
      continue;
    }
    if(packet_len == srv_users[i]->username_len &&
    !strncmp(
      srv_users[i]->username, 
      (char *) packet,
      packet_len
    )) {
      srv_err(fd, "Username is taken.");
      return;
    };
  }
  if(free_space == -1){
    srv_err(fd, "Earth is closed, today.");
    return;
  }
  
  srv_user_t* user = malloc(sizeof(srv_user_t));
  char *name = malloc(packet_len);
  if(!(user && name)){
    srv_die(fd, "Failed to allocate user.");
    exit(1);
  }
  user->username = name;
  user->username_len = packet_len;
  strncpy(user->username, (char *) packet, packet_len);
  // printf("wrote username %s\n", user->username);
  srv_users[free_space] = user;
  // printf("username in srv_users: %s\n", srv_users[free_space]->username);
  srv_res(fd,0,0,"");
}

void srv_handle_logout(int fd, uint8_t* packet, uint16_t packet_len){
  if(!(srv_curr_user)){
    srv_err(fd, "You are not logged in.");
    return;
  }
  srv_res(fd,0,0,"");
}

void srv_handle_add(int fd, pkt_inst_add_t* header, uint8_t* packet, uint16_t packet_len){
  if(!(srv_curr_user)){
    srv_err(fd, "You are not logged in.");
    return;
  }
  if(header->index >= MAX_PASSWORDS || header->index < 0){
    srv_err(fd, "Invalid slot.");
    return;
  }
  if(srv_curr_user->passwords[header->index].password){
    srv_err(fd, "Slot is taken.");
    return;
  }
  char *pw = malloc(packet_len);
  if(!pw){
    srv_die(fd, "Failed to allocate password.");
    exit(1);
  }
  memcpy(pw, packet, packet_len);
  srv_curr_user->passwords[header->index].password = pw;
  srv_curr_user->passwords[header->index].len = packet_len;
  srv_res(fd,0,0,"");
}

void srv_handle_get(int fd, pkt_inst_get_t* header){
  if(!(srv_curr_user)){
    srv_err(fd, "You are not logged in.");
    return;
  }
  srv_pw_t *pw = &srv_curr_user->passwords[header->index];
  if(!pw->password){
    srv_err(fd, "Slot is empty.");
    return;
  }
  srv_res(fd,0,pw->len,pw->password);
}

void srv_handle_del(int fd, pkt_inst_del_t* header){
  if(!(srv_curr_user)){
    srv_err(fd, "You are not logged in.");
    return;
  }
  if(header->index >= MAX_PASSWORDS || header->index < 0){
    srv_err(fd, "Invalid slot.");
    return;
  }
  srv_pw_t *pw = &srv_curr_user->passwords[header->index];
  if(!pw->password){
    srv_err(fd, "Slot is empty.");
    return;
  }
  free(pw->password);
  pw->password = 0;
  pw->len = 0;
  srv_res(fd,0,0,0);
}


void srv_handle_bug(int fd, pkt_inst_del_t* header, uint8_t* packet, uint16_t packet_len){
  srv_res(fd,0,0,0); //todo
}

void srv_handle_pkt(int fd, uint8_t * header, uint8_t *packet, uint16_t packet_len){
  switch(header[0]){
    case PKT_HELO:
      srv_handle_helo(fd, packet, packet_len); break;
    case PKT_SIGNUP:
      srv_handle_signup(fd, packet, packet_len); break;
    case PKT_LOGOUT:
      srv_handle_logout(fd, packet, packet_len); break;
    case PKT_ADD:
      srv_handle_add(fd, (void *) header, packet, packet_len); break;
    case PKT_GET:
      srv_handle_get(fd, (void *) header); break;
    case PKT_DEL:
      srv_handle_del(fd, (void *) header); break;
    case PKT_BUG:
      srv_handle_bug(fd, (void *) header, packet, packet_len); break;
  }
}

void srv_parse_pkt(int fd, srv_parse_state_t* state, uint8_t *in_buf, int len){
  while(len){
    // printf("srv state %d, len=%d\n", state->state, len);
    switch(state->state){
      case SRV_PARSE_INIT:
        // printf("srv init state\n");
        state->i = 0;
        state->identifier = in_buf[0];
        state->state = SRV_PARSE_HDR;
        state->header_length = 0;
        state->packet = 0;
        continue;
        break; // for good measure
      case SRV_PARSE_HDR:
        // printf("srv hdr state, i=%d\n", state->i);
        // printf("current byte %02x\n", in_buf[0]);
        state->header[state->i] = in_buf[0];
        state->i++;
        switch(state->identifier){
          case PKT_HELO:
            state->header_length = sizeof(pkt_inst_helo_t);
            break;
          case PKT_SIGNUP:
            state->header_length = sizeof(pkt_inst_signup_t);
            break;
          case PKT_LOGOUT:
            state->header_length = sizeof(pkt_inst_bye_t);
            break;
          case PKT_ADD:
            state->header_length = sizeof(pkt_inst_add_t);
            break;
          case PKT_GET:
            state->header_length = sizeof(pkt_inst_get_t);
            break;
          case PKT_DEL:
            state->header_length = sizeof(pkt_inst_del_t);
            break;
          case PKT_BUG:
            state->header_length = sizeof(pkt_inst_bug_t);
            break;
        }
        if(state->i == state->header_length){
          // printf("\nsrv: parsed header\n----\n");
          // printf("header len %d\n", state->header_length);
          // printf("i %d\n", state->i);
          // printf("header: ");
          // hex_dump(state->header_length, state->header);
          uint8_t _has_body= *((uint8_t *) &state->header[state->header_length - 3]);
          if(!_has_body){
            state->state = SRV_PARSE_DISPATCH;
            continue;
          }
          state->data_length = *((uint16_t *) &state->header[state->header_length - 2]);
          if(!state->data_length){
            srv_err(fd, "Invalid packet");
            state->state = SRV_PARSE_INIT;
          }
          else {
            state->packet = malloc(state->data_length);
            if(!state->packet){
              state->state = SRV_PARSE_DISPATCH;
              continue;
            }
            memset(state->packet, 0, state->data_length);
            state->data = state->packet;
            state->i = state->data_length;
            state->state = SRV_PARSE_DATA;
          }
        }
        break;
      case SRV_PARSE_DATA:
        // printf("srv data state, len: %d\n", state->data_length);
        state->data[0] = in_buf[0];
        state->data_length--;
        state->data++;
        if(!state->data_length){
          state->state = SRV_PARSE_DISPATCH;
          continue;
        }
        break;
    }
    if(state->state == SRV_PARSE_DISPATCH){
      // printf("srv handling\n");
      srv_handle_pkt(fd, state->header, state->packet, state->i);
      if(state->packet){
        free(state->packet);
      }
      state->state = SRV_PARSE_INIT;
    }

    len -= 1;
    in_buf++;
  }
}

void srv_loop(int fd){
  uint8_t rcv[512];
  int num_rcv;
  srv_parse_state_t parse_state;
  parse_state.state = SRV_PARSE_INIT;
  srv_users = malloc(sizeof(srv_user_t *) * MAX_USERS);
  close(0);
  close(1);
  close(2);

  while(1){
    num_rcv = 0;
    if((num_rcv = read(fd, rcv, 64)) <= 0){
      printf("[!] Connection closed or died unexpectedly.\n");
      return;
    }
    // printf("\nsrv received %d bytes:\n", num_rcv);
    // hex_dump(num_rcv, rcv);
    srv_parse_pkt(fd, &parse_state, rcv, num_rcv);
  }
  free(srv_users);
}

int main(int argc, char **argv){
  int fds[2];  

  setvbuf(stdin, 0, _IONBF, 0);
  setvbuf(stdout, 0, _IONBF, 0);
  setvbuf(stderr, 0, _IONBF, 0);
  
  //just pretend like this is some sort of real network connection
  socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, fds);
  if(fork()){
    close(fds[0]);
    setuid(0xdeadbeef);
    client(fds[1]);
  }
  else {
    close(fds[1]);
    setuid(1000);
    srv_loop(fds[0]);
  }
}