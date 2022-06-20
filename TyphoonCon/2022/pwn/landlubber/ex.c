#include <fcntl.h>
#include <malloc.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>


// Runtime assert, assumes libc error
#define ASSERT(p, s)            if (!(p))\
                                {\
                                    puts(s);\
                                    exit(1);\
                                }

#define WIN_ASSERT(p, s)        if (!(p))\
                                {\
                                    printf("%ld - %lx - %s\n", GetLastError(), GetLastError(), s);\
                                    exit(1);\
                                }

#define NET_ASSERT(c, s)        WIN_ASSERT(((c) != NETWORK_ERROR), s)
#define FD_ASSERT(c, s)         WIN_ASSERT(((c) != FD_ERROR), s)

#define ARRAY_LEN(x)            (sizeof(x) / sizeof(*(x)))

// Not necessary, just more performant than getting an EBADF
#define CLOSE_IF(fd)            if ((fd) != 0)\
                                {\
                                    close((fd));\
                                }
#define ALLOC_VEC(vec, l)       do {\
                                    ASSERT(((l) + sizeof((vec)->len)) > (l), "Too big length, malloc would overflow");\
                                    ASSERT((vec) = malloc((l) + sizeof((vec)->len)), "Failed allocating vec");\
                                    (vec)->len = (l);\
                                } while (0);

#define NETWORK_ERROR           (-1)
#define FD_ERROR                (-1)
#define GOOD_PORT_NUM           (0x1337)
#define SIGNATURE_FILE_EXT      (".sig")
#define SECRET_PASS             ("xxREDACTED!xx")
#define SHA256_DIGEST_LENGTH    (0x20)

typedef void (*cmd_func)(const int sock);

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpedantic"
struct vec
{
    size_t len;
    char data[0];
};
#pragma GCC diagnostic pop


char * strndup(const char * const src, size_t n)
{
    size_t len = strlen(src);
    size_t to_copy = len > n ? n : len;
    char * ret = malloc(to_copy + 1);

    memcpy(ret, src, to_copy);
    ret[to_copy] = 0;

    return ret;
}

struct vec * recv_var_data(const int sock)
{
    struct vec * recv_data = NULL;
    size_t to_read = 0;
    size_t read_so_far = 0;
    uint32_t len = 0;

    NET_ASSERT(recv(sock, (void *)&len, sizeof(len), MSG_WAITALL), "recving command");

    to_read = len;
    ALLOC_VEC(recv_data, len);

    while (to_read > read_so_far)
    {
        NET_ASSERT(len = recv(sock, (void *)(recv_data->data + read_so_far), to_read - read_so_far, MSG_WAITALL), "recv() failure");
        read_so_far += len;
    }

    return recv_data;
}


void dump_data_to_file(const char * const filename, const char * const data, const DWORD len)
{
    const int file_fd = open(filename, O_WRONLY | O_CREAT | O_BINARY | O_TRUNC, 0644);

    FD_ASSERT(file_fd, "Failed creating file");

    FD_ASSERT(write(file_fd, data, len), "Failed writing to file");

    close(file_fd);
}

void get_module(const int sock)
{
    puts("GET MODULE");

    struct vec * filename = NULL;
    struct vec * sig = NULL;
    struct vec * file_data = NULL;
    char * sig_filename = NULL;
    char * filename_null_terminated = NULL;

    filename = recv_var_data(sock);
    sig = recv_var_data(sock);
    file_data = recv_var_data(sock);

    WIN_ASSERT(sig_filename = malloc(filename->len + sizeof(SIGNATURE_FILE_EXT)), "Couldn't allocate signature file name");
    memcpy(sig_filename, filename->data, filename->len);
    memcpy(sig_filename + filename->len, SIGNATURE_FILE_EXT, sizeof(SIGNATURE_FILE_EXT));

    if (strstr(sig_filename, "/") != NULL)
    {
        goto cleanup;
    }

    dump_data_to_file(sig_filename, sig->data, sig->len);
    filename_null_terminated = strndup(filename->data, filename->len);
    dump_data_to_file(filename_null_terminated, file_data->data, file_data->len);

cleanup:
    free(filename_null_terminated);
    free(sig_filename);
    free(file_data);
    free(sig);
    free(filename);
}

struct vec * read_file_data(const char * const filename)
{
    int file_fd = 0;
    struct vec * recvd_data = NULL;
    size_t len = 0;

    FD_ASSERT(file_fd = open(filename, O_RDONLY | O_BINARY), "Failed opening file for read");

    len = lseek(file_fd, 0, SEEK_END);
    lseek(file_fd, 0, SEEK_SET);

    ALLOC_VEC(recvd_data, len);

    FD_ASSERT(read(file_fd, recvd_data->data, recvd_data->len), "Failed reading file data");
    close(file_fd);

    return recvd_data;
}

void kmac_file(unsigned char * const out, const struct vec * const file_data)
{
    HCRYPTPROV crypt_prov = {0};
    HCRYPTHASH sha_hasher = {0};
    DWORD len = SHA256_DIGEST_LENGTH;

    CryptAcquireContextA(&crypt_prov, NULL, NULL, PROV_RSA_AES, CRYPT_DELETEKEYSET); // Allowed to Fail (it's okay that we don't catch it, since its entire point is to make the next call work)
    WIN_ASSERT(CryptAcquireContextA(&crypt_prov, NULL, NULL, PROV_RSA_AES, CRYPT_NEWKEYSET), "Failed CryptAcquireContext");
    WIN_ASSERT(CryptCreateHash(crypt_prov, CALG_SHA_256, 0, 0, &sha_hasher), "Failed CryptCreateHash");
    WIN_ASSERT(CryptHashData(sha_hasher, (void *)SECRET_PASS, strlen(SECRET_PASS), 0), "Failed CryptHashData #1");
    WIN_ASSERT(CryptHashData(sha_hasher, (void *)file_data->data, file_data->len, 0), "Failed CryptHashData #2");
    WIN_ASSERT(CryptGetHashParam(sha_hasher, HP_HASHVAL, out, &len, 0), "Failed CryptGetHashParam");
}

void load_module(const char * const filename, const int sock)
{
    HMODULE mod = NULL;
    FARPROC func_ptr = NULL;

    WIN_ASSERT(mod = LoadLibrary(filename), "Failed LoadLibrary!");
    WIN_ASSERT(func_ptr = GetProcAddress(mod, "run_tests"), "Failed finding function in library");

    func_ptr(sock);

    FreeLibrary(mod);
}

void run_module(const int sock)
{
    puts("RUN MODULE");

    struct vec * filename = NULL;
    struct vec * sig_data = NULL;
    char * filename_for_real = NULL;
    char * sig_filename_for_real = NULL;
    struct vec * file_data = NULL;
    unsigned char kmac_res[SHA256_DIGEST_LENGTH] = {0};

    filename = recv_var_data(sock);
    filename_for_real = strndup(filename->data, filename->len);
    file_data = read_file_data(filename_for_real);

    if (strstr(filename_for_real, "/") != NULL)
    {
        goto cleanup;
    }

    kmac_file(kmac_res, file_data);

    sig_filename_for_real = malloc(filename->len + sizeof(SIGNATURE_FILE_EXT));
    strcpy(sig_filename_for_real, filename_for_real);
    memcpy(sig_filename_for_real + filename->len, SIGNATURE_FILE_EXT, sizeof(SIGNATURE_FILE_EXT));

    sig_data = read_file_data(sig_filename_for_real);

    if (sig_data->len != SHA256_DIGEST_LENGTH)
    {
        goto cleanup;
    }

    if (memcmp(sig_data->data, kmac_res, sig_data->len) == 0)
    {
        printf("%s is good!\n", filename_for_real);
        load_module(filename_for_real, sock);
    }
    else
    {
        printf("%s is bad!\n", filename_for_real);
        goto cleanup;
    }

cleanup:
    free(file_data);
    free(sig_filename_for_real);
    free(sig_data);
    free(filename_for_real);
    free(filename);
}

void handle_connection(const int sock)
{
    uint8_t command = 0;
    cmd_func cmd_funcs[] = {get_module, run_module};

    while (1)
    {
        NET_ASSERT(recv(sock, (void *)&command, sizeof(command), MSG_WAITALL), "recving command");

        if (command >= ARRAY_LEN(cmd_funcs))
        {
            return;
        }

        cmd_funcs[command](sock);
    }
}

// Straight up copied from MSDN
void startup()
{
    WORD wVersionRequested;
    WSADATA wsaData;

    wVersionRequested = MAKEWORD(2, 2);

    ASSERT(WSAStartup(wVersionRequested, &wsaData) == 0, "Failed WSAStartup");
    ASSERT((LOBYTE(wsaData.wVersion) == 2) && (HIBYTE(wsaData.wVersion) == 2), "Incorrect WSA version");
}

int main()
{
    int sock = 0;
    int recvd_sock = 0;
    struct sockaddr_in any = {0};
    struct sockaddr_in recvd = {0};
    int recvd_addr_len = sizeof(recvd);

    startup();

    any.sin_family = AF_INET;
    any.sin_port = htons(GOOD_PORT_NUM);
    any.sin_addr.s_addr = INADDR_ANY;

    NET_ASSERT(sock = socket(AF_INET, SOCK_STREAM, 0), "initializing listener sock");
    NET_ASSERT(bind(sock, (struct sockaddr *)(&any), sizeof(any)), "binding listener sock");
    NET_ASSERT(listen(sock, 1), "listen listener sock");

    while (1)
    {
        NET_ASSERT(recvd_sock = accept(sock, (struct sockaddr *)(&recvd), &recvd_addr_len), "accept on main sock");

        handle_connection(recvd_sock);

        CLOSE_IF(recvd_sock);
    }

    CLOSE_IF(sock);
    WSACleanup();
}
