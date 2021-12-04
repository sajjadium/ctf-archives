#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jemalloc/jemalloc.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>

#define MAX 16
#define DATA_SIZE 0x48
#define KEY_SIZE 0x8

long alloc_min;
long alloc_max;
long libjemalloc_min;
long libjemalloc_max;

typedef struct User{
	char *key;
	char username[DATA_SIZE];
	char password[DATA_SIZE];
	char personal_data[DATA_SIZE];
} User;

User *users[MAX] = { NULL };


void init(){
	User *admin = (User *) malloc(sizeof(User));
	uid_t uid = geteuid();
	setreuid(uid, uid);
	alloc_min = ((unsigned long)admin >> 0x14) << 0x14;
	alloc_max = alloc_min + 0x400000;
	libjemalloc_min = (unsigned long)&malloc - 0x95fc;
	libjemalloc_max = libjemalloc_min + 0x270000;
	free(admin);
}

bool check_personal_key(unsigned long ptr){
	if(ptr > alloc_min && ptr < alloc_max){
		return true;
	}
	else if(ptr > libjemalloc_min && ptr < libjemalloc_max){
		return true;
	}
	else{
		return false;
	}
}


void welcome(){
	printf("1.  Allocate a user\n");
	printf("2.  Edit the username\n");
	printf("3.  Edit the password\n");
	printf("4.  Edit the personal data\n");
	printf("5.  Delete a user\n");
	printf("6.  Show the user personal key\n");
	printf("7.  edit the user personal key\n");

}

int get_index(void) {
	for(int i = 0; i < MAX; i++){
		if(users[i] == NULL){
			return i;
		}
	}
	_exit(-1);
}

int check_index(int index){
	if(index < 0 || index >= MAX) _exit(-1);
	return index;
}

void xor(char *data, char *key){
	for(int i = 0; i < strlen(data); i++){
		data[i] = data[i] ^ key[i % KEY_SIZE];
	}
}

void add_null_at_end(char *data, int offset){
	if(data[offset - 1] == '\n'){
		data[offset - 1] = '\0';
	}
}

bool empty_password(char *password){
	if(strlen(password) == 0) _exit(-1);
}

bool check_password(int index){
	bool is_valid = false;
	printf("Enter the size of your password: ");
	int n;
	scanf("%d", &n);
	char *password = (char *) alloca(n);
	printf("Enter the password: ");
	read(0, password, n);
	add_null_at_end(password, n);
	empty_password(users[index]->password);
	if(strlen(password) != strlen(users[index]->password)){
		return 0;
	}
	xor(users[index]->password, users[index]->key);
	if(strcmp(password, users[index]->password) == 0){
		is_valid = true;
	}
	xor(users[index]->password, users[index]->key);
	return is_valid;
}

void allocate_user(void) {
	int index = get_index();
	int end;

	User *get_user = (User *) malloc(sizeof(User));
	printf("Enter your username: ");
	end = read(0, get_user->username, DATA_SIZE);
	add_null_at_end(get_user->username, end);
	printf("Enter your password: ");
	end = read(0, get_user->password, DATA_SIZE);
	add_null_at_end(get_user->password, end);
	empty_password(get_user->password);
	printf("Enter your personal data: ");
	end = read(0, get_user->personal_data, DATA_SIZE);
	add_null_at_end(get_user->personal_data, end);
	printf("Enter a key to secure your password and personal data: ");
	get_user->key = (char *) malloc(KEY_SIZE);
	end = read(0, get_user->key, KEY_SIZE);
	add_null_at_end(get_user->key, end);

	xor(get_user->password, get_user->key);
	xor(get_user->personal_data, get_user->key);

	users[index] = get_user;
}




void delete_key(int index){
	memset(users[index]->key, 0, KEY_SIZE);
	free(users[index]->key);
	users[index]->key = NULL;
}


void delete_user(void) {
	int index;
	printf("Enter the user you want to delete: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	delete_key(index);
	free(users[index]);
	users[index] = NULL;
}

void edit_username(void) {
	int index;
	printf("Enter the user you want to edit the username: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	printf("Enter the new username: ");
	memset(users[index]->username, 0, DATA_SIZE);
	int end = read(0, users[index]->username, DATA_SIZE);
	add_null_at_end(users[index]->username, end);
	return;
}

void edit_password(void){
	int index;
	printf("Enter the user you want to edit the password: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	printf("Enter the new password: ");
	memset(users[index]->password, 0, DATA_SIZE);
	int end = read(0, users[index]->password, DATA_SIZE);
	add_null_at_end(users[index]->password, end);
	empty_password(users[index]->password);
	xor(users[index]->password, users[index]->key);
	return;
}

void edit_personal_data(void){
	int index;
	printf("Enter the user you want to edit the personal data: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	printf("Enter the new personal data: ");
	memset(users[index]->personal_data, 0, DATA_SIZE);
	int end = read(0, users[index]->personal_data, DATA_SIZE);
	add_null_at_end(users[index]->personal_data, end);
	xor(users[index]->personal_data, users[index]->key);
	return;
}



void show_personal_key(){
	int index;
	printf("Enter the user you want to get the personal key: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	if(check_personal_key((unsigned long) users[index]->key)); 
		printf("%s\n", users[index]->key);

}

void edit_personal_key(){
	int index;
	printf("Enter the user you want to edit the personal key: ");
	scanf("%d", &index);
	check_index(index);
	if(users[index] == NULL) _exit(-1);
	if(check_password(index) == 0) return;
	if(check_personal_key((unsigned long) users[index]->key)){
		printf("Enter the new personal key: ");
		xor(users[index]->password, users[index]->key);
		xor(users[index]->personal_data, users[index]->key);
		memset(users[index]->key, 0, KEY_SIZE);
		read(0, users[index]->key, KEY_SIZE);
		xor(users[index]->password, users[index]->key);
		xor(users[index]->personal_data, users[index]->key);
	}
}



int main(void) {
	int choice;
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	init();
	while(1) {
		welcome();
		printf("Enter the choice: ");
		scanf("%d", &choice);
		switch(choice) {
			case 1:
				allocate_user();
			break;
			case 2:
				edit_username();
			break;
			case 3:
				edit_password();
			break;
			case 4:
				edit_personal_data();
			break;
			case 5:
				delete_user();
			break;
			case 6:
				show_personal_key();
			break;
			case 7:
				edit_personal_key();
			break;
			default:
			return 0;
		}
	}
}