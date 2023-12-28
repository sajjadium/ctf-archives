#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <malloc.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/wait.h>
#include <ctype.h>
#include <sys/mman.h>
#include <string.h>
#include <errno.h>
#include <dirent.h>
#include <signal.h>

#include "base64.h"
#include "signature.h"

#define KB 1024

#define HTTP_SIMPLE_PAGE(msg) ("HTTP/1.0 200 OK\r\n"\
                        "Content-Type: text/html; charset=UTF-8\r\n\r\n"\
                        "<doctype !html><html><head><title></title>"\
                        "<style>body"\
                        "h1 { font-size:4cm; text-align: center; color: black;"\
                        "}</style></head>"\
                        "<body><h1>" msg "</h1></body></html>\r\n")


#define ANONYMOUS_USER_JSON "{'user': 'anonymous', 'signed_up': 'unknown', 'last_login': 'unknown', 'favorite_cheese': 'unknown', 'role': 'user'}"


#define HTTP_RESP_UNAVAILABLE HTTP_SIMPLE_PAGE("Service Unavailable (HTTP 503)")

#define HTTP_RESP_FILE_NOT_FOUND HTTP_SIMPLE_PAGE("File not Found (HTTP 404)")

#define printf_err_v(msg, ...) printf("[%s:%d] " msg, __FILE__, __LINE__, __VA_ARGS__)

#define printf_err(msg) printf("[%s:%d] " msg, __FILE__, __LINE__)

#define ROLE_UNAUTHENTICATED (-1)
#define ROLE_USER (0)
#define ROLE_ADMIN (1)

//Originally from https://stackoverflow.com/questions/34052975/using-multi-thread-build-a-simple-http-server-in-c
//All credit to Groundins

/*function declerations*/
void send_content(int fd, int connfd,int isDir,char* path);
void enqueue(int data);
void* dequeue(void* ptr);
int send_to_client(int connfd, char* line);
int check_authorization(char* buf, int buf_len, int connfd);
int gen_token(char* json, char* buf, size_t buf_len);
/*global vars*/
pthread_mutex_t lock;
pthread_cond_t emp;
int sock =0;
int max_threads =0;
int global_count=0;
int finished =1;
int length=0;
/*Queue*/
struct node{
    int info;
    struct node *ptr;
}*head,*tail;
struct sigaction ready, last;

RSA* rsa_priv;
RSA* rsa_pub;

void init_priv_key()
{
    FILE* keyFile = fopen("admin/key.pem", "r");
    fseek(keyFile, 0, SEEK_END);
    long fsize = ftell(keyFile);
    fseek(keyFile, 0, SEEK_SET);  /* same as rewind(f); */

    char *key = malloc(fsize + 1);
    if(keyFile!=NULL && fread(key, fsize, 1, keyFile)>0)
    {
        rsa_priv = createPrivateRSA(key);
        //printf("priv: %p\n", rsa_priv);
    }
    if(!rsa_priv)
    {
        printf_err("Couldn't load private key\n");
        fclose(keyFile);
        free(key);
        exit(1);
    }
    free(key);
    fclose(keyFile);
}

void init_pub_key()
{
    FILE* keyFile = fopen("admin/key.pub", "r");
    fseek(keyFile, 0, SEEK_END);
    long fsize = ftell(keyFile);
    fseek(keyFile, 0, SEEK_SET);  /* same as rewind(f); */

    char *key = malloc(fsize + 1);
    if(keyFile!=NULL && fread(key, fsize, 1, keyFile)>0)
    {
        rsa_pub = createPublicRSA(key);
        //printf("pub: %p\n", rsa_pub);
    }
    if(!rsa_pub)
    {
        printf_err("Couldn't load public key\n");
        fclose(keyFile);
        free(key);
        exit(1);
    }
    free(key);
    fclose(keyFile);
}

void init_keys()
{
    init_priv_key();
    init_pub_key();
}

int main(int argc, char** argv){
    int threads;
    int requests; 
    int port;
    int i; 
    int len_of_packet=1;
    int thrd ;
    int rc;
    unsigned int addr_size;
    struct sockaddr_in serv_addr, client_addr;
    static fd_set socks;
    int servfd; 
    int socket_of_accept; 
    assert (argc ==3 || argc ==4);

    init_keys();

    threads = strtol(argv[1], NULL, 10);
    if ((errno == ERANGE && (threads == LONG_MAX || threads == LONG_MIN))
            || (errno != 0 && threads == 0)) {
        perror("Error: strtol has been failed\n");
        exit(0);
    }
    max_threads = threads;
    requests = strtol(argv[2], NULL, 10);
    if ((errno == ERANGE && (requests == LONG_MAX || requests == LONG_MIN))
            || (errno != 0 && requests == 0)) {
        perror("Error: strtol has been failed\n");
        exit(0);
    }
    port = 80; 
    if (argc == 4){
        port = strtol(argv[3], NULL, 10);
        if ((errno == ERANGE && (port == LONG_MAX || port == LONG_MIN))
                || (errno != 0 && port == 0)) {
            perror("Error: strtol has been failed\n");
            exit(0);
        }
    }
    pthread_t threadsArr[threads];

    if(pthread_mutex_init(&lock,NULL)!=0){
        printf_err("Error: failed to init mutex\n");
        return 1;   
    }
    pthread_cond_init( &emp, NULL);

    head=NULL;
    tail=NULL;
    /*create threads*/
    for (thrd=0; thrd<threads;thrd++){
        rc = pthread_create(&threadsArr[thrd], NULL,  dequeue, (void*) &thrd);
        if (rc){
            printf_err("Error: failed to create thread\n");
            return 1;   
        }
    }
    /* create socket */
    servfd = socket(AF_INET, SOCK_STREAM, 0);
    sock = servfd;
    if (servfd == -1) {
        printf_err("Error creating socket\n");
        exit(1);
    }
    /* init prepernces */
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(port);
    /* bind */
    setsockopt(servfd, SOL_SOCKET, SO_REUSEADDR, (const char *) &len_of_packet,sizeof(int));
    if (bind(servfd, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) == -1) {
        printf_err("Error: Bind has been failed\n");
        perror ("Bind: ");
        exit(1);
    }
    /*listen */
    if (listen(servfd, requests) == -1) {
        printf_err("Error: Listen has been failed\n");
        perror ("Listen: ");
        exit(1); 
    }
    FD_ZERO(&socks);
    FD_SET(servfd, &socks);

    while(1){
        sigfillset(&ready.sa_mask);
        ready.sa_handler = SIG_IGN;
        ready.sa_flags = 0;
        if (sigaction(SIGINT, &ready,&last) || sigaction(SIGINT,&last,NULL)){
            printf("Exiting\n");
            finished=0;
            for(i=0; i<threads; i++){
                rc = pthread_join(threadsArr[i], NULL);
                if(rc != 0){
                    printf_err("Error: join has been failed\n");
                    perror("Join: ");
                    return 1;   
                }
            }
            pthread_mutex_destroy(&lock);
            close(sock);
        }

        addr_size = sizeof(client_addr);
        socket_of_accept = accept(servfd, (struct sockaddr *) &client_addr, &addr_size);
        if (socket_of_accept == -1) {
            printf_err("Error: Accept has been failed\n");
            perror ("Accept: ");
            exit(1);
        }

        enqueue(socket_of_accept);

    }
    return 0;
}

void process_connection(int socket_of_accept)
{
    char buf[KB] ;
    char Uniform_Resource_Identifier[KB];
    char method[KB];
    char path[KB];
    int s_len = 0; 
    int r_len = 0;
    int role = -1;
    
    memset(buf, 0, sizeof(buf));
    memset(Uniform_Resource_Identifier, 0, sizeof(Uniform_Resource_Identifier));
    memset(method, 0, sizeof(method));
    memset(path, 0, sizeof(path));
    /*recieve message*/
    r_len = recv(socket_of_accept, buf, KB,0);
    if (r_len == -1){
        printf_err_v("Error: receive has failed on %d\n", socket_of_accept);
        close(socket_of_accept);
        return;
    }
    sscanf(buf,"%s %s", method, Uniform_Resource_Identifier);
    sscanf(Uniform_Resource_Identifier,"%s", path);
    role = check_authorization(buf, KB, socket_of_accept);
    printf("method = %s, path = %s role = %d\n", method, path, role);
    /*GET OR POST*/
    if(strcmp(method, "GET")!= 0 && strcmp(method, "POST") != 0){
        char response[] = HTTP_RESP_UNAVAILABLE;
        s_len = send(socket_of_accept, response, strlen(response), 0);
        if (s_len == -1){
            printf_err_v("Error: failed to send message %s to client %d\n", response, socket_of_accept);
            close(socket_of_accept);
            return;
        }
        close(socket_of_accept);
    }
    else if (strncmp(path, "/token", 6)==0)
    {
        char response[20*KB];
        strcpy(response, "HTTP/1.0 200 OK\r\n\r\n");
        char *resp = response+strlen(response);
        if(gen_token(ANONYMOUS_USER_JSON, resp, sizeof(response))<=0)
            strcpy(response, HTTP_SIMPLE_PAGE("500 Internal Server Error"));
        s_len = send(socket_of_accept, response, strlen(response), 0);
        if (s_len == -1){
            printf_err_v("Error: failed to send message %s to client %d\n", response, socket_of_accept);
            close(socket_of_accept);
            return;
        }
        close(socket_of_accept);
    }
    else if(strncmp(path, "/admin/flag", 11)==0)
    {
        if(role == ROLE_ADMIN)
        {
            int f = open("admin/flag", O_RDONLY);
            send_content(f, socket_of_accept, 0, NULL);
            close(f);
        }
        else
        {
            char response[] = HTTP_RESP_FILE_NOT_FOUND;
            s_len = send(socket_of_accept, response, strlen(response), 0);
            if (s_len == -1){
                printf_err_v("Error: failed to send message %s to client %d\n", response, socket_of_accept);
                close(socket_of_accept);
                return;
            }
        }
        close(socket_of_accept);
    }
    else{ /*file not found*/
        char response[] = HTTP_RESP_FILE_NOT_FOUND;
        s_len = send(socket_of_accept, response, strlen(response), 0);
        if (s_len == -1){
            printf_err_v("Error: failed to send message %s to client %d\n", response, socket_of_accept);
            close(socket_of_accept);
            return;
        }
        close(socket_of_accept);
    }
}

void send_content(int fd, int connfd,int isDir,char* path){
    char line[KB];
    memset(line, 0, sizeof(line));
    if (!send_to_client(connfd, "HTTP/1.0 200 OK\r\n\r\n"))
    {
        printf_err_v("Failed to send to client: %d\n", connfd);
        return;
    }
    int return_value;
    if(!isDir){
        while ((return_value=read(fd, line, KB)) > 0) {
            if(!send_to_client(connfd, line))
            {
                printf_err_v("Failed to send to client: %d\n", connfd);
                memset(line, 0, sizeof(line));
                return;
            }
            memset(line, 0, sizeof(line));
        }
        if (return_value < 0){
            perror("Error read");
            if(!send_to_client(connfd, "Error Resorces\n"))
            {
                printf_err_v("Failed to send to client: %d\n", connfd);
                return;
            }
            return;
        }
    }
    else {
        DIR           *d;
        struct dirent *dir;
        d = opendir(path);
        if (d)
        {
            while ((dir = readdir(d)) != NULL)
            {
                strcpy(line,dir->d_name);
                strcat(line,"\n");
                if(!send_to_client(connfd,line))
                {
                    printf_err_v("Failed to send to client: %d\n", connfd);
                    break;
                }
                memset(line, 0, sizeof(line));
            }
            closedir(d);
        }
    }
}

/*enqueue*/
void enqueue(int data)
{
    int rc;
    struct node* temp;
    temp = (struct node *)malloc(1*sizeof(struct node));
    if(temp == NULL){
        printf_err("Error: couldn't allocate memory\n");
        exit(1);
    }
    temp->ptr = NULL;
    temp->info = data;
    if (pthread_mutex_lock(&lock) !=0){
        printf_err("Error: failed to lock\n");
        exit(1);
    } 

    if (length == 0) /*empty queue*/
    {
        head = temp;
    }else 
    {
        tail->ptr = temp; 
    }
    tail = temp;
    length++;
    //printf("%d\n",length);
    if (pthread_mutex_unlock(&lock)!=0){
        printf_err("Error: failed to unlock\n");
        pthread_exit(0);
    }
    rc = pthread_cond_broadcast(&emp);
    assert(rc==0);
    //printf("Enqueue return\n");
    return;
}


int send_to_client(int connfd, char* line){
    int nsent, totalsent;
    int notwritten = strlen(line);
    /* keep looping until nothing left to write*/
    totalsent = 0;
    while (notwritten > 0){
        /* notwritten = how much we have left to write
            totalsent  = how much we've written so far
            nsent = how much we've written in last write() call */
        nsent = write(connfd, line + totalsent, notwritten);
        if(nsent<0) // check if error occured (client closed connection?)
        {
            return 0;
        }
        totalsent  += nsent;
        notwritten -= nsent;
    }
    return 1;
}



/*dequeue*/
void* dequeue(void* ptr)
{
    int rc;
    struct node* temp;
    while(finished){

        if (pthread_mutex_lock(&lock) !=0){
            printf_err("Error: lock has been failed\n");
            pthread_exit(0);
        }

        while (length == 0)
        {
            rc = pthread_cond_wait(&emp, &lock);
            assert(rc == 0);
        }
        int info = head->info;
        temp = head;
        head = head->ptr;
        free(temp);

        length--;
        //printf("%d\n",length);
        if (pthread_mutex_unlock(&lock)!=0){
            printf_err("Error: unlock has been failed\n");
            pthread_exit(0);
        }
        rc = pthread_cond_broadcast(&emp);
        assert(rc==0);
        process_connection(info);
    }
    printf("Thread Exiting\n");
    pthread_exit(0);
}

char* get_auth_header(char* buf, int buf_len, int connfd)
{
    char* line = strtok(buf, "\n");
    while(line)
    {        
        char* last_line = line;

        line = strtok(NULL, "\n");
        if(line)
        {
            //printf("%s\n",last_line);
            if(strlen(last_line)<=1)
            {
                return NULL;
            }
            if(strncmp(last_line, "Authorization: ", 15)==0)
            {
                return last_line+15;
            }
        }
        //If no line is found check if there is more to read, but we just won't support that, respect the MTU folks.
    }
    return NULL;
}

int gen_token(char* json, char* buf, size_t buf_len)
{
    unsigned char* sig_buf;
    size_t sig_len = 0;
    RSASign(rsa_priv, (unsigned char*)json, strlen(json), &sig_buf, &sig_len);
    if (!sig_buf)
    {
        printf_err_v("Couldn't sign JSON. %s\n", json);
        return -1;
    }
    size_t sig_enc_len = 0;
    char *sig_enc_buf = base64_encode((unsigned char*)sig_buf, sig_len, &sig_enc_len);
    size_t json_enc_len = 0;
    char *json_enc_buf= base64_encode((unsigned char*)json, strlen(json), &json_enc_len);

    if(sig_enc_len+json_enc_len>buf_len-2)
    {
        printf_err_v("Generated token too long. json: %d, sig: %d\n", (int)json_enc_len, (int)sig_enc_len);
        free(sig_buf);
        free(json_enc_buf);
        free(sig_enc_buf);
        return -1;
    }

    strncpy(buf, json_enc_buf, json_enc_len);
    buf[json_enc_len] = '.';
    strncpy(buf+json_enc_len+1, sig_enc_buf, sig_enc_len);
    buf[json_enc_len+sig_enc_len+1] = 0;
    free(sig_buf);
    free(json_enc_buf);
    free(sig_enc_buf);
    return json_enc_len+sig_enc_len+1;
}

int parse_role(char* auth_json)
{
    printf("json: %s\n", auth_json);
    char* json = strchr(auth_json, '{')+1;
    json = strtok(json, "}");
    char* token = strtok(json, ",");
    while(token)
    {
        printf("token: %s\n", token);
        while(*token==' ')
            token++;
        if(strncmp(token, "'role': ", 8)==0)
        {
            char* role_str = token+8;
            if(strncmp(role_str, "'admin'", 7)==0)
                return ROLE_ADMIN;
            else if(strncmp(role_str, "'user'", 7)==0)
                return ROLE_USER;
        }
        usleep(100000);
        token = strtok(NULL, ",");
    }
    return ROLE_UNAUTHENTICATED;
}

int check_authorization(char* buf, int buf_len, int connfd)
{
    char* auth_header = get_auth_header(buf, buf_len, connfd);
    if(!auth_header)
        return ROLE_UNAUTHENTICATED;

    //printf("Authorization: %s\n", auth_header);

    if(strncmp(auth_header, "Bearer ", 7)==0)
    {
        char* auth_str = auth_header+7;

        char* dotIdx = strchr(auth_str, '.');
        if(!dotIdx)
            return ROLE_UNAUTHENTICATED;
        *dotIdx = 0;
        unsigned char* signature = (unsigned char*)dotIdx+1;

        size_t sig_len = 0;
        size_t auth_len = 0;
        auth_str = (char*)base64_decode(auth_str, strlen(auth_str), &auth_len);

        //printf("len: %ld, signature: %s\n", strlen((char*)signature), signature);
        signature = base64_decode((char*)signature, strlen((char*)signature)-1, &sig_len);
        //printf("auth_str: %s\n", auth_str);
        //printf("auth_len: %ld\tsig_len: %ld\n", auth_len, sig_len);

        bool authentic = 0;
        if(RSAVerifySignature(rsa_pub, signature, sig_len, auth_str, auth_len, &authentic))
        {
            if(authentic)
            {
                int result = parse_role(auth_str);
                free(auth_str);
                free(signature);
                return result;
            }
        }
        free(auth_str);
        free(signature);
    }

    return ROLE_UNAUTHENTICATED;
}