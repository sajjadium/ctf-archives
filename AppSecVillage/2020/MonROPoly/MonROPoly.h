

extern void print(char *);
void init_window(),printBoard(),winrefresh(),createBoard(),print(char *string), get(char *string,int a),init_game(),editName(),printOptions(),printwin4(),changeLoc(int,int,int),clearGadgets(),toggleAnimation();
extern void printwin3(char *);
extern void gotoJail();
extern void get(char *,int);
extern void push(int,int);
extern void pop();
extern void clearGadgets();
extern void changeLoc(int, int, int);
extern int main();
extern WINDOW *win4;
extern void init_window();
extern void editName();
typedef struct player{
	char name[24];
	int i;
	int j;
	int isPlayer;
}Player;

Player *player;

void (*chance[14])();
int chancecheck[14] = {0};
//chance card functions
unsigned long long gadgets[8][8];
char * gadgetsString[8][8];


void chance0(){
	printwin3("Your time is up go to jail");
	gotoJail();
}

//this seems a bit too powerful
void chance1(){
	printwin3("You inherited a Gadget\n What address would you like?\n Send as decimal");
	char tmp[21];
	get(tmp,20);
	long long address = atoll(tmp);
	gadgets[6][7] = address;
	push(6,7);
}

void chance5();
void chance2(){
	long long address = (long long)(((unsigned long long)chance5&0xfffffffffffff000)-0x1000);
	printwin3("You found a vulnerable printf\n What offset would you like to leak?\n Send as decimal");
	char tmp[21];
	get(tmp,20);
	int offset = atoi(tmp);
	endwin();
	printf("Leak: %s\n", address+offset);
	fflush(stdout);
	sleep(3);
	init_window();
	//leak based off offset of program
}

void chance3(){
	printwin3("Advance to POP RDI!");
	player->i = 6;
	player->j = 3;
	changeLoc(player->i,player->j,1);
	push(6,3);

	//move player to pop rdi
}

void chance4(){
	printwin3("Advance to Leave!");
	player->i = 1;
	player->j = 0;
	
	changeLoc(player->i,player->j,1);
	push(1,0);
	//mov player to leave, check for passing go
}

void chance5(){
	printwin3("Advance to POP RSI, POP R15!");
	player->i = 3;
	player->j = 6;
	changeLoc(player->i,player->j,1);
	push(3,6);
	//same as 4
}

void chance6(){
	printwin3("Go to start");
	player->i = 6;
	player->j = 0;
	changeLoc(player->i,player->j,1);
	push(6,0);
	//mov player
}

void chance7(){
	printwin3("Your bug did not qualify as a CVE\n Lose Last Gadget");
	pop();
	//pop gadget	
}

void chance8(){
	printwin3("You found a sketchy looking website.\n A random value has been added to your chain");
	gadgets[6][7] = rand();
	push(6,7);
	//add random value, probably stick with 32 bit
}

void chance9(){
	printwin3("Life insurance matures collect $100");
	//do nothing, maybe show a new title of current money
}

void chance10(){
	printwin3("You found an Arbitrary write\n Where would you like to write to?\n Send as Decimal");
	char tmp[21];
	get(tmp,20);
	long long current = atoll(tmp);

	printwin3("What 2 byte value would you like?\n Send as Decimal");
	get(tmp,5);
	short value = atoi(tmp);
	*((short *)current)=value;

	//ask for where and what, thinking 4 bytes whould be enough for the write
}

void chance11(){
	printwin3("You have been audited\n Lose All your Gadgets");
	clearGadgets();
	//lose all gadgets
}

void chance12(){
	printwin3("Luck is on your side\n POPA has been added to your gadgets");
	push(7,7);
	//add popa
}
void chance13(){
	printwin3("You get to choose a new name");
	editName();	
}


void init_chance(){
        chance[0] = chance0;

	//chance[1] = chance1;

        chance[2] = chance2;

        chance[3] = chance3;

        chance[4] = chance4;

        chance[5] = chance5;

        chance[6] = chance6;

        chance[7] = chance7;

        chance[8] = chance8;

        chance[9] = chance9;

        chance[10] = chance10;

        chance[11] = chance11;

        chance[12] = chance12;

	chance[13] = chance13;

        return;
}

void helper(){
	asm("pop %rdi; ret; pop %rsi; pop %r15; ret;pop %rbp; ret;pop %rax; ret;mov %rdi, %rsi; ret; pop %rdx; ret; mov %rax, %rdi; ret; pop %rcx; ret; syscall; ret; mov $0xdeadbeefcafebabe, %rcx; push %rcx; ret; leave; ret");

}
char flag[] = "flag.txt";
char binsh[] = "/bin/!!";//darn so close

void init_gadgets(){
	//there will be some overlap with the edges but I think that should be fine
	gadgets[0][0] = -3;//jail
	gadgets[0][1] = (unsigned long long)(helper+44);//pop rbp
	gadgets[0][2] = (unsigned long long)(helper+18);//pop rdx
	gadgets[0][3] = (unsigned long long)(helper+12);//pop rax
	gadgets[0][4] = -2;//chance
	gadgets[0][5] = (unsigned long long)&flag;//pushflag.txt
	gadgets[0][6] = -3;//freeparking
	
	gadgets[6][0] = 0;//start push 0
	gadgets[6][1] = (unsigned long long)(helper+26);//syscall
	gadgets[6][2] = -4;//pay tax lose last gadget
	gadgets[6][3] = (unsigned long long)(helper+4);// pop rdi
	gadgets[6][4] = -2;//chance
	gadgets[6][5] = 2;//push 2
	gadgets[6][6] = -1;//lose all gadgets & go to jail
	//maybe set the ones that are functions to a specific value so that my push can notice and do something with them. negative value?
	gadgets[1][0] = (unsigned long long)(helper+41);//leave
	gadgets[2][0] = -2;//chance
	gadgets[3][0] = 1;//mov push 1
	gadgets[4][0] = (unsigned long long)(helper+29);//push deadbeefcafebabe
	gadgets[5][0] = (unsigned long long)(helper+14);//mov rsi, rdi

	gadgets[1][6] = (unsigned long long)(helper+20);//mov rdi, rax
	gadgets[2][6] = -2;//chance
	gadgets[3][6] = (unsigned long long)(helper+6);//pop rsi, r15
	gadgets[4][6] = (unsigned long long)(helper+24);//pop rcx
	gadgets[5][6] = 40;//push 40

	gadgetsString[0][0] = 0;//jail
	gadgetsString[0][1] = malloc(25);//pop rbp
	gadgetsString[0][2] = malloc(25);//pop rdx
	gadgetsString[0][3] = malloc(25);//pop rax
	gadgetsString[0][4] = 0;//chance
	gadgetsString[0][5] = malloc(25);//pushflag.txt
	gadgetsString[0][6] = 0;//freeparking

	gadgetsString[6][0] = malloc(25);//start
	gadgetsString[6][1] = malloc(25);//syscall
	gadgetsString[6][2] = 0;//pay tax lose last gadget
	gadgetsString[6][3] = malloc(25);// pop rdi
	gadgetsString[6][4] = 0;//chance
	gadgetsString[6][5] = malloc(25);//push 2
	gadgetsString[6][6] = 0;//lose all gadgets & go to jail
	//maybe set the ones that are functions to a specific value so that my push can notice and do something with them. negative value?
	gadgetsString[1][0] = malloc(25);//leave
	gadgetsString[2][0] = 0;//chance
	gadgetsString[3][0] = malloc(25);//mov push 1
	gadgetsString[4][0] = malloc(25);//push deadbeefcafebabe
	gadgetsString[5][0] = malloc(25);//mov rsi, rdi

	gadgetsString[1][6] = malloc(25);//mov rdi, rax
	gadgetsString[2][6] = 0;//chance
	gadgetsString[3][6] = malloc(25);//pop rsi, r15
	gadgetsString[4][6] = malloc(25);//pop rcx
	gadgetsString[5][6] = malloc(25);//push 40

	strcpy(gadgetsString[0][1],"POP RBP");//pop rbp
	strcpy(gadgetsString[0][2],"POP RDX");//pop rdx
	strcpy(gadgetsString[0][3],"POP RAX");//pop rax
	strcpy(gadgetsString[0][5],"PUSH FLAG.TXT");//pushflag.txt

	strcpy(gadgetsString[6][0],"PUSH 0");//start
	strcpy(gadgetsString[6][1],"SYSCALL");//syscall
	strcpy(gadgetsString[6][3],"POP RDI");// pop rdi
	strcpy(gadgetsString[6][5],"PUSH 2");//push 2

	strcpy(gadgetsString[1][0],"LEAVE");//leave
	strcpy(gadgetsString[3][0],"PUSH 1");//mov push 1
	strcpy(gadgetsString[4][0],"PUSH 0XDEADBEEFCAFEBABE");//push deadbeefcafebabe
	strcpy(gadgetsString[5][0],"MOV RSI, RDI");//mov rsi, rdi

	strcpy(gadgetsString[1][6],"MOV RDI, RAX");//mov rdi, rax
	strcpy(gadgetsString[3][6],"POP RSI, POP R15");//pop rsi, r15
	strcpy(gadgetsString[4][6],"POP RCX");//pop rcx
	strcpy(gadgetsString[5][6],"PUSH 40");//push 40

	gadgetsString[7][7] = malloc(25);
	strcpy(gadgetsString[7][7],"POPA");
	gadgets[7][7] = 0;//popa
	gadgetsString[6][7] = malloc(25);
	strcpy(gadgetsString[6][7],"CUSTOM");



}
