#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <dirent.h>

int max_request_size = 2 << 20; // 1 MiB

#define RETURN_ADDR_OFFSET 0x1010
#define HTTP_METHOD_GET 0x0
#define HTTP_METHOD_POST 0x1

char *list_dir(char *path) {
    DIR *dirp;
    struct dirent *dent;

    char *resp_begin = "<!doctype html>\n<html>\n<body>\n <ul>\n";
    char *resp_end = " </ul>\n</body>\n";

    int resplen = strlen(resp_begin) + strlen(resp_end);
    if ((dirp = opendir(path)) == NULL) {
        perror("opendir");
        return NULL;
    }

    while ((dent = readdir(dirp)) != NULL) {
        resplen += 2*strlen(dent->d_name) + strlen("  <li> <a href=\"\"></li>\n");
    }

    char *buf = malloc(resplen+1);
    buf[0] = '\0';

    strcat(buf, resp_begin);

    seekdir(dirp, 0);
    while ((dent = readdir(dirp)) != NULL) {
        //if (strcmp(dent->d_name, ".") == 0 || strcmp(dent->d_name, "..") == 0) {
        //    continue;
        //}
        strcat(buf, "  <li> <a href=\"");
        strcat(buf, dent->d_name);
        strcat(buf, "\">");
        strcat(buf, dent->d_name);
        strcat(buf, "</li>\n");
    }
    closedir(dirp);

    strcat(buf, resp_end);
    return buf;
}

char * parse_path(char *buf) {
    char *pathstart = strstr(buf, " ")+1;
    char *pathend;
    if ((pathend = strstr(pathstart, " ")) == NULL) {
        perror("Malformed Header");
        return NULL;
    }
    pathend = strstr(pathstart, "?") < pathend && strstr(pathstart, "?") != NULL ? strstr(pathstart, "?") : pathend;
    int pathlen = pathend - pathstart;
    printf("pathlen: %d\n", pathlen);
    char *path;
    if (asprintf(&path, "./%.*s", pathlen, pathstart) == -1) {
        perror("asprintf");
        return NULL;
    }
    return path;
}

char * get_query_string(char *buf) {
    char *pathstart = strstr(buf, " ")+1;
    char *querystart;
    // return empty string instead?
    if ((querystart = strstr(pathstart, "?")) == NULL) {
        return NULL;
    }
    char *queryend;
    if ((queryend = strstr(querystart, " ")) == NULL) {
        return NULL;
    }
    querystart++;
    int querylen = queryend - querystart;
    char *querystring = malloc(querylen + 1);
    strncpy(querystring, querystart, querylen);
    return querystring;
}

int handle_connection(int connfd) {
    char buf[4096];
    int received = 0;
    //char resp_header[4096];
    char *resp_body;
    int status = 200;
    char *status_string;
    void *addr_choice = NULL;

    memset(buf, '\0', 4096);
    received = recv(connfd, buf, 4095, 0);
    printf("%s\n", buf);

    if (received == -1) {
        perror("recv");
        // Internal Server Error?
    }

    if (strstr(buf, "\r\n\r\n") == NULL) {
        status = 400;
        status_string = "Bad Request";
    }

    int http_method;
    if (strncmp(buf, "GET ", 4) == 0) {
        http_method = HTTP_METHOD_GET;
    }
    else if (strncmp(buf, "POST ", 5) == 0) {
        http_method = HTTP_METHOD_POST;
    }
    else {
        status = 405;
        status_string = "Method Not Allowed";
    }

    char *path;
    if ((path = parse_path(buf)) == NULL) {
        perror("parse_path");
        status = 400;
        status_string = "Bad Request";
    }
    printf("request for path %s\n", path);

    //char *http_version_end = strstr(queryend+1, "\r\n");
    char *http_version_end = strstr(strstr(strstr(buf, " ")+1, " ")+1, "\r\n");
    *http_version_end = '\0';

    if (status == 200) {
        status_string = "OK";
        if ((resp_body = list_dir(path)) == NULL) {
            perror("list_dir");
            status = 400;
            status_string = strerror(errno);
            asprintf(&resp_body, "%s\n", status_string);
        }
    }
    else {
        asprintf(&resp_body, "%s\n", status_string);
    }

    // send response header
    dprintf(connfd, "%s %d %s\r\n\r\n", strstr(strstr(buf, " ")+1, " ")+1, status, status_string);

    // send response body
    if (resp_body != NULL) {
        send(connfd, resp_body, strlen(resp_body), 0);
    }

    // free resources
    free(path);
    free(resp_body);

    // here, I'll just let you write a ROP chain. Without an address leak you won't be able to do anything anyways!
    if (http_method == HTTP_METHOD_POST) {
        //char *req_header_end = strstr(buf, "\r\n\r\n")+4;
        char *req_header_end = strstr(http_version_end+1, "\r\n\r\n")+4;
        int roplen = received - (req_header_end - buf);
        roplen = roplen > 128 ? 128 : roplen;
        memcpy(buf+RETURN_ADDR_OFFSET+8, req_header_end, roplen);
        //memcpy(buf+RETURN_ADDR_OFFSET+8, req_header_end, received - (req_header_end - buf));
    }

    return 0;
}

int main(int argc, char *argv[])
{
    int sockfd, connfd;
    int ret;
    socklen_t connlen;
    struct sockaddr_in sockaddr;
    struct sockaddr_storage connaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    u_int yes = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, &yes, sizeof(yes)) == -1) {
        perror("setsockopt");
    }
    memset(&sockaddr, 0, sizeof(sockaddr));
    sockaddr.sin_family = AF_INET;
    sockaddr.sin_port = htons(1337);
    sockaddr.sin_addr.s_addr = INADDR_ANY;
    if (bind(sockfd, (struct sockaddr*)&sockaddr, sizeof(sockaddr)) == -1) {
        perror("bind");
    }

    if (listen(sockfd, 0) == -1) {
        perror("listen");
    } 

    while (1) {
        pid_t pid;
        connlen = sizeof connaddr;
        memset(&connaddr, 0, connlen);
        connfd = accept(sockfd, (struct sockaddr*)&connaddr, &connlen);
        if (connfd == -1) {
            perror("accept");
        }
        pid = fork();
        if (pid == 0) {
            ret = handle_connection(connfd);
            printf("back in main!\n");
            shutdown(connfd, 2);
            exit(0);
        }
        close(connfd);
    }


    return EXIT_SUCCESS;
}
