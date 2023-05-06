#include <openssl/aes.h>
#include <openssl/md5.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <lz4.h>

void read_flag();
void read_key();
static void sign();
static void verify();

AES_KEY key;

void read_key()
{
	unsigned char key_buf[16];

	FILE* urandom = fopen("/dev/urandom", "rb");
	if (!urandom) exit(EXIT_FAILURE);
	if (fread(key_buf, 16, 1, urandom) != 1) exit(EXIT_FAILURE);
	if (fclose(urandom)) exit(EXIT_FAILURE);

	AES_set_encrypt_key(key_buf, 128, &key);
}

typedef struct
{
	unsigned char data[16];
} digest;

digest hash(unsigned char* buffer, size_t len)
{
	digest d;
	if (MD5(buffer, len, d.data) != d.data) exit(EXIT_FAILURE);
	return d;
}

digest mac(unsigned char* buffer, size_t len)
{
	digest d = hash(buffer, len);

	digest mac;
	AES_encrypt(d.data, mac.data, &key);

	return mac;
}

__attribute__((always_inline))
static inline void sign()
{
	unsigned char buffer[0xc0];
	unsigned char msg[0x100];

	printf("Message: ");
	size_t len = read(STDIN_FILENO, buffer, sizeof(buffer));
	digest m = mac(buffer, len);

	int decomp_size = LZ4_decompress_safe(buffer, msg, len, sizeof(msg) - 1);
	if (decomp_size < 0)
	{
		printf("Error decompressing message.\n");
		exit(EXIT_FAILURE);
	}
	msg[decomp_size] = 0;

	printf("Signature: ");
	for (unsigned int j = 0; j < sizeof(m.data); j++)
		printf("%02x", m.data[j]);
	printf("\n");
	printf("For: %s\n", msg);
}

__attribute__((always_inline))
static inline void verify()
{
	unsigned char buffer[0xc0];
	unsigned char msg[0x100];
	memset(msg, 0, sizeof(msg));

	printf("Message: ");
	size_t len = read(STDIN_FILENO, buffer, sizeof(buffer));
	digest m = mac(buffer, len);

	printf("Signature: ");
	digest sig;
	for (unsigned int j = 0; j < sizeof(sig.data); j++)
		scanf("%02hhx", &sig.data[j]);

	if (memcmp(sig.data, m.data, sizeof(sig.data)))
	{
		printf("Invalid signature!\n");
		exit(EXIT_FAILURE);
	}

	LZ4_decompress_safe(buffer, msg, len, 0x1000);

	printf("Verified message: %s\n", msg);
}

void menu()
{
	printf("0: Sign a message\n");
	printf("1: Verify a message\n");

	while (true)
	{
		int option;
		printf("Pick an option: ");
		scanf("%d", &option);

		if (option == 0)
			sign();
		else if (option == 1)
			verify();
		else
			break;
	}
}

void sys_exit(int status, void* arg)
{
	syscall(SYS_exit, status);
}

int main()
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	read_key();

	menu();

	return EXIT_SUCCESS;
}
