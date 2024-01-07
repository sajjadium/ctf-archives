// Here's a snippet of the source code for you

int main() {
    printf("Guess: ");
    char flag[49+8+1] = {0};
    if(scanf("%57s", flag) != 1 || strlen(flag) != 57 || strncmp(flag, "irisctf{", 8) != 0 || strncmp(flag + 56, "}", 1)) {
        printf("Guess harder\n");
        return 0;
    }
#define flg(n) *((__uint64_t*)((flag+8))+n)
    syscall(0x1337, flg(0), flg(1), flg(2), flg(3), flg(4), flg(5));
    printf("Maybe? idk bro\n");

    return 0;
}
