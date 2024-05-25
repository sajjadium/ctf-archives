#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>
#include <dirent.h>

/* Maximum length of a username, password, and list item */
#define USER_LENGTH		16
#define PASS_LENGTH		32
#define ITEM_LENGTH		64

/* Bank account record keeping structs */
struct sdobj;
typedef struct
{
	char owner[32];
	float money[2];
	struct sdobj *sdbox;
} __attribute__((__packed__)) account_t;

typedef struct
{
	int date;
	float amount_num;
	char paid_to[32];
	char amount_str[40];
	char address[32];
	char memo[28];
} __attribute__((__packed__)) check_t;

typedef struct sdobj
{
	char name[32];
	char desc[64];
	char owner[32];
	float size;
	struct sdobj *next;
} __attribute__((__packed__)) sdobj_t;

char user[USER_LENGTH];
char prog_dir[64];
account_t account;

static char *readline(char *buffer, int len, FILE *fp)
{
	if (fgets(buffer, len, fp) == NULL) return NULL;
	buffer[strcspn(buffer, "\n")] = 0;

	if (buffer[0] == 0) return NULL;
	else return buffer;
}

static void writeline(char *buffer, int len, FILE *fp)
{
	int newline_idx = strcspn(buffer, "\0");
	if (newline_idx == len) newline_idx = len - 1;

	buffer[newline_idx] = '\n';
	fwrite(buffer, newline_idx + 1, 1, fp);
}

static bool valid_string(char *str)
{
	for (char *s = str; *s != 0; s++) if (*s == '/' || *s == '.') return false;
	return true;
}

static float read_float(char *purpose)
{
	printf("Enter the %s as a decimal number (nn.mm): ", purpose);
	fflush(stdout);
	char buffer[16];
	readline(buffer, 16, stdin);

	int radix_idx = strcspn(buffer, ".");
	if (radix_idx >= strlen(buffer) - 1) return NAN;

	int whole = 0;
	for (int i = 0; i < radix_idx; i++)
	{
		if (buffer[i] < 0x30 || buffer[i] > 0x39) return NAN;

		whole *= 10;
		whole += buffer[i] - 0x30;
	}

	int frac = 0, fracdiv = 1;
	for (int i = radix_idx + 1; buffer[i] != 0; i++)
	{
		if (buffer[i] < 0x30 || buffer[i] > 0x39) return NAN;

		frac *= 10;
		frac += buffer[i] - 0x30;

		fracdiv *= 10;
	}

	return ((float)whole) + (((float)frac) / fracdiv);
}

static int read_account()
{
	FILE *fp = fopen(".account", "rb");
	if (!fp)
	{
		return -1;
	}

	size_t len = sizeof(account_t) - sizeof(sdobj_t*);
	if (fread(&account, 1, len, fp) != len)
	{
		goto fail;
	}

	sdobj_t tmp;
	sdobj_t *cur = NULL;
	len = sizeof(sdobj_t) - sizeof(sdobj_t*);
	while (fread(&tmp, 1, len, fp) == len)
	{
		sdobj_t *new = (sdobj_t*)malloc(sizeof(sdobj_t));
		memcpy(new, &tmp, len);
		new->next = NULL;

		if (cur == NULL) account.sdbox = new;
		else cur->next = new;

		cur = new;
	}

	return 0;

fail:
	printf("Error reading account info\n");
	exit(-1);
}

static void write_account()
{
	FILE *fp = fopen(".account", "wb");
	if (!fp)
	{
		goto fail;
	}

	size_t len = sizeof(account_t) - sizeof(sdobj_t*);
	if (fwrite(&account, 1, len, fp) != len)
	{
		goto fail;
	}

	sdobj_t *cur = account.sdbox;
	while (cur)
	{
		len = sizeof(sdobj_t) - sizeof(sdobj_t*);
		if (fwrite(cur, 1, len, fp) != len)
		{
			goto fail;
		}

		cur = cur->next;
	}

	fclose(fp);
	return;

fail:
	printf("Error saving account info\n");
	exit(-1);
}

void deposit_money()
{
	float deposit = read_float("amount to deposit");
	while (isnan(deposit))
	{
		printf("Invalid decimal number\n");
		deposit = read_float("amount to deposit");
	}
	printf("Deposit: %.2f\n", deposit);

	printf("Which account should it go to, checking or savings?\n");
	char whichaccount[16];
	int account_num = -1;
	while (account_num == -1)
	{
		readline(whichaccount, 16, stdin);

		if (strcmp(whichaccount, "savings") == 0) account_num = 0;
		else if (strcmp(whichaccount, "checking") == 0) account_num = 1;

		if (account_num != -1) break;
		printf("Invalid account\n");
	}

	account.money[account_num] += deposit;
	write_account();
}

void withdraw_money()
{
	float withdrawal = read_float("amount to withdraw");
	while (isnan(withdrawal))
	{
		printf("Invalid decimal number\n");
		withdrawal = read_float("amount to withdraw");
	}

	printf("Which account should it come from, checking or savings?\n");
	char whichaccount[16];
	int account_num = -1;
	while (account_num == -1)
	{
		readline(whichaccount, 16, stdin);

		if (strcmp(whichaccount, "savings") == 0) account_num = 0;
		else if (strcmp(whichaccount, "checking") == 0) account_num = 1;

		if (account_num != -1) break;
		printf("Invalid account\n");
	}

	if (withdrawal <= account.money[account_num])
	{
		account.money[account_num] -= withdrawal;
		write_account();
	}
	else printf("Not enough money in the account!\n");
}

void view_money()
{
	printf("Savings: %.2f\t\t\tChecking: %.2f\n", account.money[0], account.money[1]);
}

void write_check()
{
	check_t *check = (check_t*)malloc(sizeof(check_t));

	check->date = (int)time(NULL);

	check->amount_num = read_float("check value");
	while (isnan(check->amount_num))
	{
		printf("Invalid decimal number\n");
		check->amount_num = read_float("check value");
	}

	printf("Enter the check value in words: ");
	fflush(stdout);
	readline(check->amount_str, 40, stdin);

	printf("Enter the recipient: ");
	fflush(stdout);
	readline(check->paid_to, 32, stdin);

	printf("Enter your address: ");
	fflush(stdout);
	readline(check->address, 32, stdin);

	printf("Enter a memo related to the check: ");
	fflush(stdout);
	readline(check->memo, 28, stdin);

	printf("\nFinal check: \n");
	printf("Date: %s\n", ctime((time_t*)&check->date));
	printf("Pay to the Order of: %s        $ %.2f\n", check->paid_to, check->amount_num);
	printf("%s Dollars\n", check->amount_str);
	printf("Address: %s\n", check->address);
	printf("Memo: %s\n\n", check->memo);
}

void store_object()
{
	sdobj_t *sdobj = (sdobj_t*)malloc(sizeof(sdobj_t));

	sdobj->size = read_float("volume of the object (in cm^3)");
	while (isnan(sdobj->size))
	{
		printf("Invalid decimal number\n");
		sdobj->size = read_float("volume of the object (in cm^3)");
	}

	if (sdobj->size > 5000.0)
	{
		printf("Object is too large\n");
		free(sdobj);
	}

	printf("Enter the short description: ");
	fflush(stdout);
	readline(sdobj->name, 32, stdin);

	printf("Enter the long description: ");
	fflush(stdout);
	readline(sdobj->desc, 64, stdin);

	printf("Enter who owns it: ");
	fflush(stdout);
	readline(sdobj->owner, 32, stdin);

	sdobj->next = NULL;

	if (account.sdbox == NULL)
	{
		account.sdbox = sdobj;
	}
	else
	{
		sdobj_t *cur = account.sdbox;
		while (cur->next) cur = cur->next;
		cur->next = sdobj;
	}

	write_account();
}

void retrieve_object()
{
	printf("Enter the # of the object: ");
	fflush(stdout);
	char num[8];
	readline(num, 8, stdin);
	unsigned int idx = atoi(num);

	sdobj_t *prev = NULL, *cur = account.sdbox;
	while (cur)
	{
		if (idx == 0)
		{
			if (prev) prev->next = cur->next;
			else account.sdbox = cur->next;
			free(cur);

			write_account();
			return;
		}
		
		prev = cur;
		cur = cur->next;
		idx--;
	}

	printf("Invalid object #\n");
}

void enumerate_objects()
{
	printf("   Name                             Owner                           \n");
	printf("--------------------------------------------------------------------\n");

	sdobj_t *cur = account.sdbox;
	int i = 0;
	while (cur)
	{
		printf("%d: %-32s %-32s\n", i, cur->name, cur->owner);

		cur = cur->next;
		i++;
	}
}

void change_password()
{
	printf("Enter a password: ");
	fflush(stdout);
	char passwd[PASS_LENGTH];
	memset(passwd, 0, PASS_LENGTH);
	readline(passwd, PASS_LENGTH, stdin);

	FILE *fp = fopen(".password", "w");
	fwrite(passwd, PASS_LENGTH, 1, fp);
	fclose(fp);
}

void login_user()
{
	chdir(prog_dir);
	chdir("users");

	bool logged_in = false;
	int fails = 0;
	do
	{
		printf("Enter username: ");
		fflush(stdout);
		readline(user, USER_LENGTH, stdin);

		if (!valid_string(user))
		{
			printf("Invalid character in username\n");
			fails++;
			continue;
		}

		int status = mkdir(user, S_IRWXG);
		if (status == 0)
		{
			chdir(user);
			change_password();
			printf("New user %s created\n", user);
			logged_in = true;
		}
		else if (status == -1 && errno == EEXIST)
		{
			chdir(user);
			
			printf("Enter password: ");
			fflush(stdout);
			char given_passwd[PASS_LENGTH];
			memset(given_passwd, 0, PASS_LENGTH);
			readline(given_passwd, PASS_LENGTH, stdin);

			FILE *fp = fopen(".password", "r");
			char real_passwd[PASS_LENGTH];
			memset(real_passwd, 0, PASS_LENGTH);
			fread(real_passwd, PASS_LENGTH, 1, fp);
			fclose(fp);

			if (strcmp(given_passwd, real_passwd) != 0)
			{
				printf("Invalid password\n");
				chdir("..");
				fails++;
				continue;
			}
			logged_in = true;
		}
		else
		{
			printf("Failed to create user directory\n");
			fails++;
		}
	} while(!logged_in && fails < 5);

	if (!logged_in) 
	{
		printf("Maximum number of failed logins exceeded\n");
		exit(-1);
	}

	if (read_account() == -1)
	{
		strncpy(account.owner, user, USER_LENGTH);
		account.money[0] = account.money[1] = 0.0;
		account.sdbox = NULL;
		
		write_account();
	}
}

void print_help()
{
	printf("d - Deposit money in an account\n");
	printf("w - Withdraw money from an account\n");
	printf("v - View account balance\n");
	printf("c - Write a check for an account\n");
	printf("s - Store an object in a safe deposit box\n");
	printf("r - Retrieve an object from a safe deposit box\n");
	printf("e - Enumerate all the items in a safe deposit box\n");
	printf("p - Change the user's password\n");
	printf("l - Login as a different user\n");
	printf("h - Print this very menu\n");
	printf("x - Exit the program\n\n");
}

void main_loop()
{
	printf("> ");
	fflush(stdout);

	char cmd[4];
	while (readline(cmd, 3, stdin))
	{
		switch (cmd[0])
		{
		case 'd':
			deposit_money();
			break;
		case 'w':
			withdraw_money();
			break;
		case 'v':
			view_money();
			break;
		case 'c':
			write_check();
			break;
		case 's':
			store_object();
			break;
		case 'r':
			retrieve_object();
			break;
		case 'e':
			enumerate_objects();
			break;
		case 'p':
			change_password();
			break;
		case 'l':
			login_user();
			break;
		case 'h':
			print_help();
			break;
		case 'x':
			exit(0);
			break;
		default:
			break;
		}

		printf("> ");
		fflush(stdout);
	}
}

int main(int argc, char **argv)
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("Welcome to GNT Holdings, the most secure bank in the world!\n");
	printf("You can deposit/withdraw money, write checks, and store your possessions safely\n\n");

	printf("Let's start by getting you logged in\n");
	getcwd(prog_dir, 64);
	login_user();

	printf("Welcome, %s! Here are the commands you can use: \n", user);
	print_help();
	main_loop();
}
