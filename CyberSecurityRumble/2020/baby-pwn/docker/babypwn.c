#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <assert.h>
#include <openssl/md5.h>

void calc_string_md5(char *string, char md5[MD5_DIGEST_LENGTH]) {
    MD5_CTX c;
    MD5_Init(&c);
    MD5_Update(&c, string, strlen(string));
    MD5_Final(md5, &c);
}

unsigned char char_to_repr(char in) {
    if (in >= '0' && in <= '9')
	return in - '0';
    if (in >= 'a' && in <= 'f')
	return in - 'a' + 0xa;
    if (in >= 'A' && in <= 'F')
	return in - 'A' + 0xa;
    assert("not in hex digit range" && 0);
}

void hex_to_binary(char *in, unsigned char* out, size_t length) {
    size_t i;
    assert("length must be even" && (length % 2) == 0);

    length /= 2;
    for (i = 0; i < length; i++) {
        out[i] = char_to_repr(in[i * 2]) << 4 | char_to_repr(in[i * 2 + 1]);
    }
}

int check_user_hash(char* flag) {
    unsigned char user_md5[MD5_DIGEST_LENGTH * 2 + 1];
    unsigned char flag_md5[MD5_DIGEST_LENGTH];
    
    /* calculate MD5("CSR{...}") */
    calc_string_md5(flag, flag_md5);
    
    /* read user input, convert to hexadecimal */
    gets(user_md5);
    hex_to_binary(user_md5, user_md5, strlen(user_md5));
    
    return memcmp(flag_md5, user_md5, MD5_DIGEST_LENGTH) ? 0 : 1;
}

int main() {
    char flag[0x500];
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    /* read flag */
    int fd = open("flag.txt", O_RDONLY);
    assert("unable to open flag file" && fd >= 0);
    flag[read(fd, flag, sizeof(flag))] = '\0';
    close(fd);

    puts("It's easy. Give me MD5($flag), get $flag in return.");

    /* if md5 is correct, print flag */
    if(check_user_hash(flag)) {
        puts(flag);
    } else {
        puts("nope");
    }

    return 0;
}
