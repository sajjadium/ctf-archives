#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

void hex_string_to_byte_array(char *hex_str, char *byte_arr, int size)
{
    int byte_ind = 0;
    for (int count = 0; count < size; count += 2)
    {
        sscanf(&hex_str[count], "%2hhx", &byte_arr[byte_ind]);
        byte_ind++;
    }
}

// this can also easily be used for memory leaks
void print_buf(unsigned char *buf, int sz)
{
    for (int i = 0; i < sz; i++)
    {
        printf("%02X", buf[i]);
    }
    puts("\n");
}

void this_function_literally_prints_the_flag()
{
    char flag[64];
    int fd = open("flag.txt", O_RDONLY);
    read(fd, flag, 64);
    puts(flag);
    close(fd);
}

void gimme_pointer()
{
    char *leak_addr;
    char this_buffer_is_definitely_too_small_for_that_read[17];
    printf("You are here: %p\n Give me an address and I will grant you 8 leaked bytes:\n", this_buffer_is_definitely_too_small_for_that_read);
    read(0, this_buffer_is_definitely_too_small_for_that_read, 64);
    hex_string_to_byte_array(this_buffer_is_definitely_too_small_for_that_read, (char *)&leak_addr, 16);
    printf("Here are the contents of %p:\n", leak_addr);
    print_buf(leak_addr, 8);
}

int main()
{
    puts("Hi! I am the Stack Oracle.\n");
    while (1)
    {
        gimme_pointer();
    }
}