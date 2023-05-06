#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

#define MAX_FILENAME_LENGTH 64
#define MAX_FILENAME_COUNT 16

char global_filename_list[MAX_FILENAME_COUNT][MAX_FILENAME_LENGTH];
int global_filename_count;

char temp_filename[MAX_FILENAME_LENGTH];
const char * read_filename()
{
    memset(temp_filename, 0, MAX_FILENAME_LENGTH);
    int l = 0;
    int c = getchar();
    while ((
            (c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') ||(c >= 'a' && c <= 'z')) &&
            l < MAX_FILENAME_LENGTH-1)
    {
        temp_filename[l++] = c;
        c = getchar();
    }
    temp_filename[l] = '\0';
   
    
    return temp_filename;
}


char temp_meta_path[MAX_FILENAME_LENGTH + 64];
const char * get_meta_path(const char * path)
{
	memset(temp_meta_path, 0, sizeof(temp_meta_path));
    strncpy(temp_meta_path, path, MAX_FILENAME_LENGTH-1);
    strcat(temp_meta_path, ".meta");
    return temp_meta_path;
}

int update_meta(const char * filename)
{
    const char * meta_path = get_meta_path(filename);
    FILE * meta_fp = fopen(meta_path, "wb+");
    if (!meta_fp) {
        puts("Error!");
        exit(-1);
    }

    struct stat st;
    if (0 != lstat(filename, &st))
	{
		printf("Error!");
		exit(-1);
	}
    fwrite(&st, sizeof(st), 1, meta_fp);
    fclose(meta_fp);
	return 0;
}
int dump_file(const char * filename)
{
	FILE * fp = fopen(filename, "rb");
	if (!fp)
	{
		puts("Error!");
		exit(-1);
	}

	char c;
	while (fread(&c, 1, 1, fp) == 1)
	{
		write(1, &c, 1);
	}
	fclose(fp);
	return 0;
}
int read_int()
{
    int l = 0;
    char buf[16];
    int c = getchar();
    while (((c >= '0' && c <= '9') || (c == '-')) && l < 15)
    {
        buf[l++] = c;
        c = getchar();
    }
    buf[l] = '\0';
    return atoi(buf);
    
}
int create()
{
    char buf[1024];
	if (global_filename_count > MAX_FILENAME_COUNT)
	{
		printf("you cannot create more file...sorry...");
		exit(-1);
	}
    printf("filename:");
    const char * filename = read_filename();

	int i;
	int exist = 0;
	
	for (i = 0; i < global_filename_count; i++)
	{
		if (strcmp(&global_filename_list[i][0], filename) == 0)
		{
			exist = 1;
		}
	}

    printf("data:");
    int l = 0;
    int c = getchar();
    while (c != '\n' && c >= 0 && c <= 255)
    {
        buf[l++] = c;
        c = getchar();
    }

    FILE * fp = fopen(filename, "a+b");
    if (!fp) {
        puts("Error!");
        exit(-1);
    }
    fwrite(buf, l, 1, fp);
    fclose(fp);
    
	update_meta(filename);
	if (!exist)
	{
		strncpy(&global_filename_list[global_filename_count][0], filename, MAX_FILENAME_LENGTH-1);
		global_filename_count += 1;
	}
}

int show()
{
    printf("filename:");
    const char * filename = read_filename();
    const char * meta_file = get_meta_path(filename);
    
    FILE * meta_fp = fopen(meta_file, "rb");
    if (!meta_fp) {
        puts("Error!");
        exit(-1);
    }

    struct stat st;
    fread(&st, sizeof(st), 1, meta_fp);
    fclose(meta_fp);

    printf("access time:%lx\n", st.st_atime);
    printf("modify time:%lx\n", st.st_mtime);
    printf("create time:%lx\n", st.st_ctime);
    
    printf("data:");

	dump_file(filename);
}
int list()
{
	int i;
	for (i = 0; i < global_filename_count; i++)
	{
		printf("%s\n", &global_filename_list[i][0]);
	}
}
int dump()
{
	write(1, &global_filename_count, sizeof(global_filename_count));

	int i;
	for (i = 0; i < global_filename_count; i++)
	{
		write(1, &global_filename_list[i][0], MAX_FILENAME_LENGTH);
		const char * filename = &global_filename_list[i][0];
		const char * meta_filename = get_meta_path(filename);
		write(1, "$$$$", 4);
		dump_file(filename);
		write(1, "$$$$", 4);
		dump_file(meta_filename);
		write(1, "$$$$", 4);
	}
	return 0;
}
int load()
{
    printf("not implemented\n");
	return 0;
}
int menu()
{
    printf("\n");
    printf("=========menu=======\n");
    printf("1. create/append file\n");
    printf("2. show file\n");
    printf("3. list\n");
    printf("4. dump file system\n");
    printf("5. load file system\n");
    printf("6. exit\n");
    printf("your choice:");
    int option = read_int();
    if (option > 6 || option < 1) return menu();
    else return option;
}
int main()
{
	global_filename_count = 0;
	memset(global_filename_list, 0, sizeof(global_filename_list));

	alarm(20);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    while (1)
    {
        int option = menu();
        switch(option)
        {
            case 1:
                create(); break;
            case 2:
                show(); break;
            case 3:
                list(); break;
            case 4:
                dump(); break;
            case 5:
                load(); break;
            case 6:
                exit(0);
        }
    }

}
