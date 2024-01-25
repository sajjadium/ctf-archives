#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

int myid;

void MPI_Encoding();

void MPI_client() {
    u_char encoding_num;
    MPI_Status status;
    char *str;
    int size;

    while (1) {
        MPI_Recv(&size, 1, MPI_INT, 0, 0xffee, MPI_COMM_WORLD, &status);
        str = malloc(size + 1);

        MPI_Recv(str, size, MPI_CHAR, 0, 0xddbb, MPI_COMM_WORLD, &status);
        str[size] = '\x00';
        
        encoding_num = 0;
        for (int i = 0; i < size; i++) {
            encoding_num ^= str[i];
        }

        MPI_Send(&encoding_num, 1, MPI_CHAR, 0, 0xaacc, MPI_COMM_WORLD);
        free(str);
    }
}

void menu() {
    printf("1. encoding\n2. terminate\n> ");
}

void MPI_server() {
    int choice;

    while(1) {
        menu();
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                MPI_Encoding();
                break;

            case 2:
                MPI_Abort(MPI_COMM_WORLD, 0);
                break;
            
            default:
                continue;
        }
    }
}

void MPI_Encoding() {
    int size, parallelism;
    MPI_Status status;
    char *str;

    // Specify the size of input and parallelism degree
    printf("Tell me the size of string to encode :");
    scanf("%d", &size);
    getchar();
    if (size <= 0 || size > 1000) {
        printf("Invalid length\n");
        return;
    }

    printf("Tell me the degree of parallelism :");
    scanf("%d", &parallelism);
    getchar();
    if (parallelism <= 0 || parallelism > 4) {
        printf("The parallelism should be among 1 - 4\n");
        return;
    }

    int str_idx = 0;
    int step = (size + parallelism - 1) / parallelism;
    for (int client_ID = 1; client_ID <= parallelism; client_ID++) {
        int partition_size = step + str_idx > size ? size - str_idx : step;
        MPI_Send(&partition_size, 1, MPI_INT, client_ID, 0xffee, MPI_COMM_WORLD);
        str_idx += step;
    }

    // Input the string
    printf("Input the string :");
    str = calloc(1, size + 1);
    fgets(str, size + 1, stdin);

    if (strlen(str) != size) {
        printf("Size of string mismatch\n");
        return;
    }

    // Divide and dispatch the tasks to clients
    str_idx = 0;
    u_char encoding_num = 0, tmp;
    for (int client_ID = 1; client_ID <= parallelism; client_ID++) {
        int partition_size = step + str_idx > size ? size - str_idx : step;
        MPI_Send(str + str_idx, partition_size, MPI_CHAR, client_ID, 0xddbb, MPI_COMM_WORLD);
        MPI_Recv(&tmp, 1, MPI_CHAR, client_ID, 0xaacc, MPI_COMM_WORLD, &status);
        encoding_num ^= tmp;
        str_idx += step;
    }

    printf("The encoding is: %u\n", encoding_num);
}

void initialize() {
    FILE *flag;
    char *gift;
    long flag_size;

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    if (myid != 0) {
        flag = fopen("./flag.txt", "r");
        fseek(flag, 0, SEEK_END);
        flag_size = ftell(flag);
        if (flag_size != 0x30) {
            printf("flag size incorrect\n");
            MPI_Abort(MPI_COMM_WORLD, 0);
        }

        rewind(flag);
        gift = calloc(1, 0x50);
        strcpy(gift, "Greeting, hacker(:");
        fread(gift + 18, flag_size, 1, flag);
        free(gift);
    }
}

int main(int argc,char *argv[])
{
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    initialize();

    if (myid == 0)
    {
        MPI_server();
    }
    else {
        MPI_client();
    }

    MPI_Finalize();
}