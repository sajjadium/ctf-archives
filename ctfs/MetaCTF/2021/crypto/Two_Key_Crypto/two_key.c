#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <inttypes.h>
#include <unistd.h>

typedef char bool;
typedef int fd;

#define TRUE 1
#define FALSE 0

void to_hex(char* out, unsigned char* buf, int len){
	for(int i = 0; i < len; i++){
		out[2 * i] = "0123456789abcdef"[buf[i] >> 4];
		out[2 * i + 1] = "0123456789abcdef"[buf[i] & 0xF];
	}
	out[2 * len] = 0;
}

bool get_server_key(unsigned char* buffer, unsigned char* iv, int max_len){
	bool success = FALSE;

	fd file = open("secret_key", O_RDONLY);
	size_t size = read(file, buffer, max_len);
	close(file);
	if(size < 8){
		puts("Invalid server key!");
		goto end;
	}

	file = open("iv", O_RDONLY);
	read(file, iv, max_len);
	close(file);

	success = TRUE;

end:
	return success;
}

bool get_user_key(unsigned char* buffer, unsigned char* IV, int max_len){
	char local_buffer[0x100];
	bool valid = FALSE;
	int actual_len = 0;

	while(!valid){
		printf("Please enter your key (up to 16 characters): ");
		fgets(local_buffer, 0x100, stdin);
		actual_len = strlen(local_buffer);
		if(local_buffer[actual_len - 1] == '\n'){
			local_buffer[actual_len - 1] = '\x00';
			actual_len -= 1;
		}

		if(actual_len > 0x10){
			puts("Your key is too long!");
		} else if(actual_len < 0x8){
			puts("Your key is too short!");
		} else {
			valid = TRUE;
		}
	}

	memcpy(buffer, local_buffer, actual_len);

	valid = FALSE;
	while(!valid){
		printf("Please enter your IV (up to 16 characters): ");
		fgets(local_buffer, 0x100, stdin);
		actual_len = strlen(local_buffer);
		if(local_buffer[actual_len - 1] == '\n'){
			local_buffer[actual_len - 1] = '\x00';
			actual_len -= 1;
		}

		if(actual_len > 0x10){
			puts("your IV is too long!");
		} else {
			valid = TRUE;
		}
	}

	memcpy(IV, local_buffer, actual_len);

	return TRUE;
}

bool get_combined_key(unsigned char* full_key, unsigned char* IV){
	bool success = FALSE;
	unsigned char server_IV[0x10];  // 128 bits
	unsigned char client_IV[0x10];  // 128 bits
	unsigned char server_key[0x10]; // 128 bits
	unsigned char client_key[0x10]; // 128 bits
	int i = 0;

	memset(server_IV, 0, 0x10);
	memset(client_IV, 0, 0x10);
	memset(server_key, 0, 0x10);
	memset(client_key, 0, 0x10);

	if(!get_server_key(server_key, server_IV, 0x10) || 
	   !get_user_key(client_key, client_IV, 0x10)){
		goto end;
	}

	/* Prepare combined key by copying the server key then xoring in the 
	 * client key (at different offsets) */
	for(i = 0; server_key[i]; i++)
		full_key[(i * 7 + 8) & 0xF] = server_key[i];
	for(i = 0; client_key[i]; i++)
		full_key[(i * 9 + 8) & 0xF] ^= client_key[i];

	/* Use the same logic for the IV as for the combined key */
	for(i = 0; server_IV[i]; i++)
		IV[(i * 7 + 8) & 0xF] = server_IV[i];
	for(i = 0; client_IV[i]; i++)
		IV[(i * 9 + 8) & 0xF] ^= client_IV[i];

	success = TRUE;

end:
	return success;
}

uint64_t get_key_schedule(unsigned char* key){
	unsigned char start = 0;
	uint64_t value = 0;

	for(int i = 0; i < 0x10; i++)
		start ^= ((i + 1) * key[i]) & 0x7F;

	/* Pick 64 bits from the 128 bit key */
	for(int i = 0; i < 64; i++){
		value = (value << 1) | ((key[start / 8] >> (start % 8)) & 1);
		start = (start * 57 + 13) % 128;	
	}

	/* Modify the key based on the selected value */
	for(int i = 0; i < 0x10; i++)
		key[i] ^= ((char*)(&value))[i % 8];

	return value;
}

void encrypt_block(unsigned char* block, unsigned char* key){
	unsigned char local_key[0x10];
	uint64_t* numblock = (uint64_t*) block;
	memcpy(local_key, key, 0x10);

	for(int i = 0; i < 32; i++){
		uint64_t itrkey = get_key_schedule(local_key);
		uint64_t left = numblock[0];
		uint64_t right = numblock[1];

		char buf[0x21];
		to_hex(buf, block, 0x10);

		left = (left ^ right) * 0xd039a8f8aa49f551ULL + 0xd37aca18132119c5ULL;
		right ^= itrkey;

		numblock[0] = right;
		numblock[1] = left;

		to_hex(buf, block, 0x10);
	}
}

void decrypt_block(unsigned char* block, unsigned char* key){
	unsigned char local_key[0x10];
	uint64_t itrkeys[0x20];
	uint64_t* numblock = (uint64_t*) block;

	memcpy(local_key, key, 0x10);

	for(int i = 0; i < 32; i++)
		itrkeys[i] = get_key_schedule(local_key);

	/* Undo what we did to encrypt the block */
	for(int i = 31; i >= 0; i--){
		uint64_t right = numblock[0];
		uint64_t left = numblock[1];

		right ^= itrkeys[i];
		/* Subtract the amount we added, then multiply by the mod inverse */
		left = ((left - 0xd37aca18132119c5ULL) * 0x376ce7a50c8a73b1ULL) ^ right;

		numblock[0] = left;
		numblock[1] = right;
	}
}

bool encrypt(unsigned char* message, int len, unsigned char* key, char* iv){
	bool success = FALSE;
	int i = 0;
	int j = 0;

	if(len % 16 != 0)
		goto end;
	
	for(i = 0; i < len; i += 16){
		for(j = 0; j < 16; j++)
			message[i + j] ^= iv[j];
		
		encrypt_block(message + i, key);
		iv = message + i;
	}

	success = TRUE;

end:
	return success;	
}

bool decrypt(char* message, int len, char* key, char* iv){
	bool success = FALSE;
	int i = 0;
	int j = 0;
	char cur_iv[16];
	char next_iv[16];

	if(len % 16 != 0)
		goto end;
	
	for(i = 0; i < len; i += 16){
		memcpy(cur_iv, iv, 16);
		memcpy(next_iv, message + i, 16);
		decrypt_block(message + i, key);

		for(j = 0; j < 16; j++)
			message[i + j] ^= cur_iv[j];

		iv = next_iv;
	}

	success = TRUE;

end:
	return success;
}

int get_flag(char* buf, int max_len){
	fd file = open("flag", O_RDONLY);
	int bytes_read = read(file, buf, max_len);
	close(file);
	return bytes_read;
}

int main(int argc, char** argv){
	setbuf(stdout, 0);
	setbuf(stdin, 0);
	setbuf(stderr, 0);
	unsigned char key[0x10];
	unsigned char iv[0x10];
	unsigned char flag[0x200];
	char out[0x401];

	memset(flag, '\x00', 0x200);
	int flag_size = get_flag(flag, 0x200);
	if(!flag_size || -1 == flag_size){
		puts("Unable to read flag");
	} else if(!get_combined_key(key, iv)){
		puts("Failed to create combined key!");
	} else {
		flag_size = (flag_size + 0xF) & ~0xF;
		encrypt(flag, flag_size, key, iv);
		to_hex(out, flag, flag_size);
		printf("%s\n", out);
	}
}
