#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <crypt.h>

//gcc Cshell.c -static -lcrypt -o Cshell
struct users {
	char name[8];
	char passwd[35];
};

struct tracker{
	struct tracker *next;
	struct users *ptr;
	char name[8];
	long int id;
};

char * alex_buff;
char * Charlie_buff;
char * Johnny_buff;
char * Eric_buff;

struct users *user;
struct users *root;

struct tracker *root_t;
struct tracker *user_t;

char *username[8];
char *userbuffer;
int uid=1000;
int length;
char salt[5] = "1337\0";
char *hash;
void setup(){
	char password_L[33];
	puts("Welcome to Cshell, a very restricted shell.\nPlease create a profile.");
	printf("Enter a username up to 8 characters long.\n> ");
	scanf("%8s",username);
	printf("Welcome to the system %s, you are our 3rd user. We used to have more but some have deleted their accounts.\nCreate a password.\n> ",username);
	scanf("%32s",&password_L);
	hash = crypt(password_L,salt);
	printf("How many characters will your bio be (200 max)?\n> ");
	scanf("%d",&length);
	userbuffer = malloc(length + 8);
	printf("Great, please type your bio.\n> ");
	getchar();
	fgets((userbuffer + 8),201,stdin);
}

void logout(){
	fflush(stdin);
	getchar();
	struct tracker *ptr;
	printf("Username:");
	char username_l[9];
	char password_l[32];
	char *hash;
	scanf("%8s",username_l);
	for (ptr = root_t; ptr != NULL; ptr = root_t->next) {


        if (strcmp(ptr->name, username_l) == 0) {
		printf("Password:");
	    scanf("%32s",password_l);
	    hash = crypt(password_l,salt);
	    if (strcmp(hash,ptr->ptr->passwd) == 0){
		    strcpy(username,ptr->name);
		    uid = ptr->id;
		    puts("Authenticated!");
		    menu();
	    }
	    else{
		    puts("Incorrect");
		    logout();
	    }
			 
        }
	else
	{
		if (ptr->next==0)
		{
			puts("Sorry no users with that name.");
			logout();
		}
	}
    }
}
void whoami(){
	printf("%s, uid: %d\n",username,uid);
	menu();
}
void bash(){

	if (uid == 0){
		system("bash");
	}
	else 
	{
		puts("Who do you think you are?");
		exit(0);
	}

}

void squad(){
	puts("..");
	menu();
}

void banner(){

puts("       /\\");
puts("      {.-}");
puts("     ;_.-'\\");
puts("    {    _.}_");
puts("    \\.-' /  `,");
puts("     \\  |    /");
puts("      \\ |  ,/");
puts("       \\|_/");
puts("");
}
void menu(){
	puts("+----------------------+");
	puts("|        Commands      |");
	puts("+----------------------+");
	puts("| 1. logout            |");
	puts("| 2. whoami            |");
	puts("| 3. bash (ROOT ONLY!) |");
	puts("| 4. squad             |");
	puts("| 5. exit              |");
	puts("+----------------------+");
	int option;
	printf("Choice > ");
	scanf("%i",&option);
	switch(option){
		case 1:
			logout();
		case 2:
			whoami();
		case 3:
			bash();
		case 4:
			squad();
		case 5:
			exit(0);
		default:
			puts("[!] invalid choice \n");
			break;
	}
}
void history(){
	alex_buff = malloc(0x40);
	char alex_data[0x40] = "Alex\nJust a user on this system.\0";
	char Johnny[0x50] = "Johnny\n Not sure why I am a user on this system.\0";
	char Charlie[0x50] ="Charlie\nI do not trust the security of this program...\0";
	char Eric[0x60] = "Eric\nThis is one of the best programs I have ever used!\0";
	strcpy(alex_buff,alex_data);
	Charlie_buff = malloc(0x50);
	strcpy(Charlie_buff,Charlie);
	Johnny_buff = malloc(0x60);
	strcpy(Johnny_buff,Johnny);
	Eric_buff = malloc(0x80);
	strcpy(Eric_buff,Eric);
	free(Charlie_buff);
	free(Eric_buff);
}

int main(){
	setvbuf(stdout, 0 , 2 , 0);
	setvbuf(stdin, 0 , 2 , 0);
	root_t = malloc(sizeof(struct tracker));
	user_t = malloc(sizeof(struct tracker));
	history();
	banner();
	user = malloc(sizeof(struct users )* 4);
	root = user + 1;
	strcpy(user->name,"tempname");
	strcpy(user->passwd,"placeholder");
	strcpy(root->name,"root");
	strcpy(root->passwd,"guessme:)");
	strcpy(root_t->name,"root");
	root_t->ptr = root;
	root_t->id = 0;
	root_t->next = user_t;
	setup();
	strcpy(user->name,username);
	strcpy(user->passwd,hash);
	strcpy(user_t->name,username);
	user_t->id=1000;
	user_t->ptr = user;
	user_t->next = NULL;
	menu();
	return 0;
}
