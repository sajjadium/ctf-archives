// gcc -Wall -Wextra -Wpedantic src.c -o chall && ./chall
#define _GNU_SOURCE 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

typedef struct Details
{
    unsigned char append_count;
    uid_t latest_owner_id;
    ino_t latest_inode;
} Details;

typedef struct FileContent
{
    char buffer[0x28];
} FileContent;

typedef struct FileContainer
{
    long root_id;
    long id;
    FileContent* content;
    Details details;
} FileContainer;

#define NUM_CONTAINERS 300
FileContainer* containers[NUM_CONTAINERS] = { 0 };
int flag_requested = 0;

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
void fatal(const char* msg)
{
    puts(msg);
    exit(EXIT_FAILURE);
}

long current_container_id = 0;
FileContainer* container_construct() {
    FileContainer* container = malloc(sizeof(FileContainer));
    if (container == NULL)
        fatal("malloc");

    container->id = current_container_id++;
    container->root_id = container->id;
    container->content = NULL;
    container->details.append_count = 0;
    container->details.latest_inode = 0;
    container->details.latest_owner_id = 9999;

    return container;
}

int container_is_equal(const FileContainer* a, const FileContainer* b) {
    return a->root_id == b->root_id && memcmp(&a->details, &b->details, sizeof(Details)) == 0;
}

void read_string(const char* msg, char* buffer, size_t nbytes)
{
    fputs(msg, stdout);
    size_t br = read(STDIN_FILENO, buffer, nbytes);
    if (br <= nbytes)
        buffer[br] = 0;
}

size_t read_int(const char* msg, size_t limit) {
    fputs(msg, stdout);
    size_t choice;
    if (scanf("%zu", &choice) != 1 || choice >= limit)
        fatal("Invalid integer input (read_int)");

    return choice;
}

void create_container()
{
    for (int i = 0; i < NUM_CONTAINERS; i++)
    {
        if (containers[i] == 0)
        {
            containers[i] = container_construct();
            printf("Created container at position: %d\n", i);
            return;
        }
    }

    puts("Full");
}

void duplicate_container()
{
    FileContainer* src = containers[read_int("FileContainer (src): ", NUM_CONTAINERS)];
    FileContainer* dst = containers[read_int("FileContainer (dst): ", NUM_CONTAINERS)];
    if (!dst || !src || dst == src)
    {
        puts("Invalid container");
        return;
    }

    dst->root_id = src->root_id;
    if (src->content) {
        FileContent* buffer = malloc(sizeof(FileContent));
        if (buffer == NULL)
            fatal("malloc");
        memset(buffer, 0, sizeof(FileContent));
        dst->content = buffer;
        strncpy(dst->content->buffer, src->content->buffer, sizeof(dst->content->buffer));
    }
    dst->details.append_count = src->details.append_count;
    dst->details.latest_owner_id = src->details.latest_owner_id;
    dst->details.latest_inode = src->details.latest_inode;
}

void prune_containers()
{
    // prune identical containers
    for (int i = 0; i < NUM_CONTAINERS; i++)
    {
        for (int j = i + 1; j < NUM_CONTAINERS; j++)
        {
            if (containers[i] == 0 || containers[j] == 0)
            {
                continue;
            }
            if (container_is_equal(containers[i], containers[j])) {
                free(containers[i]->content);
                free(containers[i]);
                containers[i] = 0;
            }
        }
    }
    puts("Flush complete");
}

void read_content()
{
    int password, bytesread, fd;
    char file_name[32] = "./";
    struct stat st;

    FileContainer* container = containers[read_int("Read into which content buffer? ", NUM_CONTAINERS)];

    if (!container) {
        puts("Invalid container");
        return;
    }

    if (container->content == 0)
    {
        FileContent* buffer = malloc(sizeof(FileContent));
        if (buffer == NULL)
            fatal("malloc");
        memset(buffer, 0, sizeof(FileContent));
        container->content = buffer;
    }
    container->details.append_count++;

    read_string("File name: ", file_name + 2, sizeof(file_name) - 2);

    if (strstr(file_name, "flag") != 0 || strstr(file_name, ".."))
        flag_requested = 1;

    *strchrnul(file_name, '\n') = 0;
    fd = open(file_name, O_RDONLY);
    if (fd == -1)
    {
        fatal("open failed on input file");
    }
    fstat(fd, &st);
    size_t file_size = st.st_size;
    container->details.latest_owner_id = st.st_uid;
    container->details.latest_inode = st.st_ino;

    read_string("Enter encryption code: ", (char*)&password, sizeof(password));
    
    // Append the file contents to the existing string in the buffer
    char* buffer = container->content->buffer;
    size_t buffer_end_pos = strlen(buffer);
    if (buffer_end_pos >= sizeof(FileContent) - 1)
    {
        puts("FileContent buffer full");
        return;
    }

    size_t nbytes = MIN(file_size, sizeof(FileContent) - 1 - buffer_end_pos);
    if ((bytesread = read(fd, buffer + buffer_end_pos, nbytes)) <= 0)
        fatal("Problem reading file");

    for (size_t i = 0; i < (size_t)bytesread; i++) {
        buffer[buffer_end_pos + i] ^= ((char*)&password)[i % sizeof(password)];
    }
    puts("File contents encrypted");
}

void print_content()
{
    int idx = read_int("Print from which file container? ", NUM_CONTAINERS);

    if (!flag_requested && containers[idx] != NULL && containers[idx]->content != NULL)
    {
        puts(containers[idx]->content->buffer);
    }
}

void menu()
{
    puts("%====== menu =======%");
    puts("1. Create container");
    puts("2. Transfer container");
    puts("3. Flush containers");
    puts("4. Reader");
    puts("5. Printer");
    puts("6. Exit");

    switch (read_int("", 7))
    {
    case 1:
        create_container();
        break;
    case 2:
        duplicate_container();
        break;
    case 3:
        prune_containers();
        break;
    case 4:
        read_content();
        break;
    case 5:
        print_content();
        break;
    case 6:
        exit(EXIT_SUCCESS);
    default:
        puts("Invalid choice");
    }
}

void setup()
{
    setbuf(stdout, 0);
    setbuf(stdin, 0);
    setbuf(stderr, 0);
}

int main()
{
    setup();
    while (1)
        menu();
}