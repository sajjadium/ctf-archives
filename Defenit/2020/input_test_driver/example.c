#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/types.h>

int main()
{
    struct input_event ie;
    int fd, fd2, ret;
    char test[10] = {0, };

    fd = open("/dev/input/event2", O_RDONLY);
    if(fd < 0) {
        perror("event2");
        return -1;
    }

    fd2 = open("/dev/input_test_driver", O_RDWR);
    if(fd < 0) {
        perror("input_test_driver");
        return -1;
    }

    test[0] = 1;
    test[1] = 2;
    test[2] = 3;
    test[3] = 4;
    test[4] = 5;

    write(fd2, test, 5);

    ioctl(fd2, 0x1337, 0); 

    while(1) {
        ret = read(fd, &ie, sizeof(struct input_event));
        if(ret < 0) {
            perror("error");
            break;
        }

        printf("type: %hu, code: %hu, value: %d \n", ie.type, ie.code, ie.value);
    }

    close(fd);
    close(fd2);

    return 0;
}
