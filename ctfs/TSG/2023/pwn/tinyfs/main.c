#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

#define NAME_MAX 0x20 - 1
#define FILE_SIZE_MAX 0x100 - 1
#define PATH_MAX 0x30 - 1
#define CACHE_MAX 0x80
#define CONTENT_MAX 0x20
#define EXEC_COMMAND(x, y, func) {int len = strlen(x); if (!strncmp(x, y, len)) { func(y + len); continue; }}

void read_n(char* ptr, int n) {
    for (int i = 0; i < n - 1; i++) {
        read(STDIN_FILENO, ptr + i, 1);
        if (*(ptr + i) == '\n') {
            *(ptr + i) = '\0';
            break;
        }
    }
    *(ptr + (n - 1)) = '\0';
}

struct MyFile {
    char content[FILE_SIZE_MAX + 1];
    char name[NAME_MAX + 1];
};

struct MyFolder {
    char name[NAME_MAX + 1];
    struct MyFolder* parent;
    struct MyFile* files[CONTENT_MAX];
    struct MyFolder* folders[CONTENT_MAX];
};

struct MyFolderCache {
    char path[PATH_MAX + 1];
    struct MyFolder* folder;
};

struct MyFolder* root;
struct MyFolder* pwd;
struct MyFolderCache cache[CACHE_MAX];

void register_cache(char* path, struct MyFolder* folder) {
    int path_len = strlen(path);
    for (int i = 0; i < CACHE_MAX; i++) {
        if (strlen(cache[i].path) == 0) {
            strcpy(cache[i].path, path);
            cache[i].folder = folder;
            break;
        }
    }
    return;
}

void delete_cache(struct MyFolder* folder) {
    for (int i = 0; i < CACHE_MAX; i++) {
        if (cache[i].folder == folder) {
            memset(&cache[i], 0, sizeof(struct MyFolderCache));
        }
    }
}

struct MyFolder* find_cache(char* path) {
    for (int i = 0; i< CACHE_MAX; i++) {
        if (!strcmp(cache[i].path, path)) {
            return cache[i].folder;
        }
    }
    return NULL;
}

int is_invalid(char* name) {
    for (int i = 0; i < strlen(name); i++) {
        if (!isalnum(name[i])) {
            puts("A name cannot contain a non-alphanumeric character.");
            return 1;
        }
    }
    return 0;
}

#define VALIDATE_NAME(name) if (is_invalid(name)) { return; }

int get_path_length(struct MyFolder* folder) {
    if (folder == root) {
        return 1;
    }
    else {
        int length = 0;
        while (folder != root) {
            length += 1 + strlen(folder->name);
            folder = folder->parent;
        }
        return length;
    }
}

void make_directory(char* name) {
    VALIDATE_NAME(name);

    if (get_path_length(pwd) + strlen(name) > PATH_MAX) {
        printf("The length of path should be shorter than or equal to %d.\n", PATH_MAX);
        return;
    }

    struct MyFolder** folder = NULL;
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->folders[i] == NULL) {
            folder = &pwd->folders[i];
        }
        else if (!strcmp(pwd->folders[i]->name, name)) {
            puts("Already exists.");
            return;
        }
    }

    struct MyFolder* new_folder = (struct MyFolder*)malloc(sizeof(struct MyFolder));
    memset(new_folder, 0, sizeof(struct MyFolder));
    strcpy(new_folder->name, name);
    new_folder->parent = pwd;
    *folder = new_folder;

    puts("A folder created.");
}

void make_file(char* name) {
    VALIDATE_NAME(name);

    if (get_path_length(pwd) + strlen(name) > PATH_MAX) {
        printf("The length of the path should be shorter than or equal to %d.\n", PATH_MAX);
        return;
    }

    struct MyFile** file = NULL;
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] == NULL) {
            file = &pwd->files[i];
        }
        else if (!strcmp(pwd->files[i]->name, name)) {
            puts("Already exists.");
            return;
        }
    }

    struct MyFile* new_file = (struct MyFile*)malloc(sizeof(struct MyFile));
    strcpy(new_file->name, name);
    *file = new_file;

    puts("A file created.");
}

void enter(char* path) {
    if (path[0] == '/') {
        // absolute path
        struct MyFolder* next_dir = find_cache(path);
        if (next_dir) {
            pwd = next_dir;
            puts("Jumped with a cache.");
            return;
        }

        char tmp[PATH_MAX + 1];
        strcpy(tmp, path);
        next_dir = root;
        char* name = strtok(tmp + 1, "/");
        while (name) {
            for (int i = 0; i < CONTENT_MAX; i++) {
                if (next_dir->folders[i] && !strcmp(next_dir->folders[i]->name, name)) {
                    next_dir = next_dir->folders[i];
                    goto NEXT;
                }
            }
            puts("The path is invalid.");
            return;
        NEXT:
            name = strtok(NULL, "/");
        }
        pwd = next_dir;
        register_cache(path, pwd);
    }
    else {
        // relative path
        VALIDATE_NAME(path);

        for (int i = 0; i < CONTENT_MAX; i++) {
            if (pwd->folders[i] && !strcmp(pwd->folders[i]->name, path)) {
                pwd = pwd->folders[i];
                return;
            }
        }

        puts("Not found.");
    }
}

void leave(char* tmp) {
    if (pwd == root) {
        puts("We are now /.");
        return;
    }

    pwd = pwd->parent;
}

void delete_item(char* name) {
    VALIDATE_NAME(name);

    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->folders[i] && !strcmp(pwd->folders[i]->name, name)) {
            for (int j = 0; j < CONTENT_MAX; j++) {
                if (pwd->folders[i]->files[j]) {
                    free(pwd->folders[i]->files[j]);
                }
            }
            delete_cache(pwd->folders[i]);
            pwd->folders[i] = NULL;
            puts("The folder has been deleted.");
            return;
        }
    }

    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] && !strcmp(pwd->files[i]->name, name)) {
            free(pwd->files[i]);
            pwd->files[i] = NULL;
            puts("The file has been deleted.");
            return;
        }
    }

    puts("The item is not found.");
}

void list_items(char* tmp) {
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->folders[i] != NULL) {
            printf("%s/\n", pwd->folders[i]->name);
        }
    }
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] != NULL) {
            printf("%s\n", pwd->files[i]->name);
        }
    }
}

void print_file_content(char* name) {
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] && !strcmp(pwd->files[i]->name, name)) {
            printf("%s\n", pwd->files[i]->content);
            return;
        }
    }

    puts("The item is not found.");
}

void write_file_content(char* name) {
    for (int i = 0; i < CONTENT_MAX; i++) {
        if (pwd->files[i] && !strcmp(pwd->files[i]->name, name)) {
            printf("Write Here > ");
            read_n(pwd->files[i]->content, FILE_SIZE_MAX);
            return;
        }
    }

    puts("The item is not found.");
}

int main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    root = (struct MyFolder*)malloc(sizeof(struct MyFolder));
    memset(root, 0, sizeof(struct MyFolder));
    root->parent = NULL;

    pwd = root;

    memset(cache, 0, sizeof(struct MyFolderCache) * CACHE_MAX);

    puts("Welcome to tinyfs");
    puts("Supported commands:");
    puts("- mkdir [dir name]: Create a directory.");
    puts("- touch [file name]: Create a file.");
    puts("- cd [dir name]: Go into the directory.");
    puts("- cd [full path]: Teleport to the directory.");
    puts("- cd ..: Leave the directory.");
    puts("- rm [dir or file name]: Delete the directory or the file.");
    puts("- ls: Displays the children of the folder.");
    puts("- cat [file name]: Read a content of the file.");
    puts("- mod [file name]: Modify a content of the file.");
    puts("- exit: Close the system.");

    while(1) {
        printf("$ ");
        char command[0x50];
        read_n(command, 0x50);
        EXEC_COMMAND("mkdir ", command, make_directory);
        EXEC_COMMAND("touch ", command, make_file);
        EXEC_COMMAND("cd ..", command, leave);
        EXEC_COMMAND("cd ", command, enter);
        EXEC_COMMAND("rm ", command, delete_item);
        EXEC_COMMAND("ls", command, list_items);
        EXEC_COMMAND("cat ", command, print_file_content);
        EXEC_COMMAND("mod ", command, write_file_content);
        if (!strcmp(command, "exit")) {
            break;
        }
        puts("Invalid.");
    }

    return 0;
}
