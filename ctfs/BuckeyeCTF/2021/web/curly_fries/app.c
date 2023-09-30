#include <curl/curl.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify_flag_file() {
    // Verify that the flag file still contains the flag
    char* buf = malloc(1024);
    FILE* fp = fopen("./flag.txt", "r");
    fgets(buf, 1024, fp);
    int res = strstr(buf, "Congratulations! Here's the flag: buckeye{") == buf;
    free(buf);
    return res;
}

char* response = NULL;
size_t response_buf_size = 0;
size_t response_size = 0;

size_t header_callback(char* data, size_t size, size_t nitems, void* userdata) {
    size_t real_size = size * nitems;

    printf("< %.*s", (int)real_size, data);

    if (strstr(data, "Content-Length") == data ||
        strstr(data, "content-length") == data) {
        __attribute__((unused)) char* name = strtok(data, " ");
        size_t content_length = atol(strtok(NULL, " "));

        if (response) {
            free(response);
        }
        response_buf_size = content_length + 1;
        response = (char*)malloc(response_buf_size);
    }
    return real_size;
}

size_t write_callback(void* data, size_t size, size_t nitems, void* userdata) {
    size_t real_size = size * nitems;

    if (response_size + real_size > response_buf_size - 1) {
        response_buf_size = response_size + real_size + 1;
        response = (char*)realloc(response, response_buf_size);
    }

    memcpy(response + response_size, data, real_size);
    response_size += real_size;
    return real_size;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    char url[64];
    printf("Enter a URL and I'll curl it: ");
    fgets(url, 64, stdin);
    url[strcspn(url, "\n")] = 0;

    if (!verify_flag_file()) {
        fprintf(stderr, "ERROR! flag.txt may have been tampered with!\n");
        return 3;
    }

    CURL* curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);

        CURLcode res = curl_easy_perform(curl);

        if (res == CURLE_OK) {
            if (response) {
                response[response_buf_size] = 0;
                puts(response);
                free(response);
            }
        } else {
            fprintf(
                stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
    }
    return 0;
}
