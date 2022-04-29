#include <stdio.h>
#include <stdlib.h>
#include <gcrypt.h>


int A(int c){
	c += 0x20;
	return c;
}
int B(int c){
	c -= 0x10;
	return c;
}
int C(int c){
	c -= 0x10;
	return c;
}
int D(int c){
	c += 0x20;
	return c;
}
int E(int c){
	c += 0x15;
	return c;
}
int F(int c){
	c -= 0x05;
	return c;
}
int G(int c){
	c += 0x25;
	return c;
}
int H(int c){
	c -= 0x35;
	return c;
}
int I(int c){
	c += 0x20;
	return c;
}
int J(int c){
	c -= 0x40;
	return c;
}

/* Simple function to perform string mangling (what is HIDE_LETTER?) */
void mangle(char * str){
	do {
		char * ptr = str;
		while (*ptr) *ptr++ = HIDE_LETTER(*ptr);
	} while(0);
}

/* Simple function to perform string unmangling (what is UNHIDE_LETTER?) */
void unmangle(char * str){
	do {
		char * ptr = str;
		while (*ptr) *ptr++ = UNHIDE_LETTER(*ptr);
	} while(0);
}


int main(){
	
	printf("Hello! This is rather embarassing:\n"
		"We have the encryption key\n"
		"We have the ciphertext (definitely!)\n"
		"We even have the IV!\n"
		"The one thing we don't have: what encryption algorithm was used to secure the flag!\n"
		"We're sure that some proof of it exists in the program, so...figure it out!\n"
		"When you're ready, type the full name, in all caps, of the constant used\n"
		"to represent the encryption library (e.g.: GCRY_CIPHER_AES128)\n"
		"If you need a hint, you can type 'hint[1-3]'\n\n");
	
	while (1){
	
		printf("Enter the name of the encryption algorithm used: \n");
	
		char response [512];
		fgets(response, 512, stdin);
		printf("response: %s\n", response);

		if (strncmp("hint1", response, 5) == 0){
			continue;
		}
		if (strncmp("hint2", response, 5) == 0){
			continue;
		}
		if (strncmp("hint3", response, 5) == 0){
			continue;
		}
		
		int size = 24;
		char *enc_alg_used = (char *)malloc(sizeof(char)*size);
		
		unmangle(enc_alg_used);		
		if (strncmp(response, enc_alg_used, strlen(enc_alg_used)) == 0){
			printf("Congrats! You got the right answer!\n");
			break;
		}
		else {
			printf("Sorry, that isn't what we were looking for. :(\n\n");
			mangle(enc_alg_used);
		}

	}

	gcry_error_t		gcry_error;
	gcry_cipher_hd_t	gcry_cipher_hd;
	size_t			index;

	size_t key_length = gcry_cipher_get_algo_keylen(GCRY_CIPHER);
	size_t block_length = gcry_cipher_get_algo_blklen(GCRY_CIPHER);
	
	char * text_buffer = (char *)malloc(sizeof(char) * 32);

	unsigned char * initialization_vector = "a test ini value";
	size_t text_length = strlen(text_buffer) + 1;
	unsigned char * encryption_buffer = malloc(text_length);
	unsigned char * out_buffer = malloc(text_length);
	unsigned char * key = "ASECRETSECRETKEY";

	gcry_error = gcry_cipher_open(&gcry_cipher_hd, GCRY_CIPHER, GCRY_CIPHER_MODE_ECB, 0);
	if (gcry_error){
		printf("gcry_cipher_open failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}

	gcry_error = gcry_cipher_setkey(gcry_cipher_hd, key, key_length);
	if (gcry_error){
		printf("gcry_cipher_setkey failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}
	
	gcry_error = gcry_cipher_setiv(gcry_cipher_hd, initialization_vector, block_length);
	if (gcry_error){
		printf("gcry_cipher_setiv failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}
	unmangle(text_buffer);
	gcry_error = gcry_cipher_encrypt(gcry_cipher_hd, encryption_buffer, text_length, text_buffer, text_length);
	if (gcry_error){
		printf("gcry_cipher_encrypt failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}

	gcry_error = gcry_cipher_setiv(gcry_cipher_hd, initialization_vector, block_length);
	if (gcry_error){
		printf("gcry_cipher_setiv failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}
	gcry_error = gcry_cipher_decrypt(gcry_cipher_hd, out_buffer, text_length, encryption_buffer, text_length);
	if (gcry_error){
		printf("gcry_cipher_decrypt failed: %s/%s\n",
				gcry_strsource(gcry_error),
				gcry_strerror(gcry_error));
		return gcry_error;
	}

	printf("Your flag is: %s\n", out_buffer); 

	return 0;
}
