#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

void divide(){
        puts("---------------------------------------------------------------------------------------\n");
}

void ascii(){
	puts("   ▄███████▄  ▄█     █▄  ███▄▄▄▄   ");
	puts("  ███    ███ ███     ███ ███▀▀▀██▄ ");
	puts("  ███    ███ ███     ███ ███   ███ ");
	puts("  ███    ███ ███     ███ ███   ███ ");
	puts("▀█████████▀  ███     ███ ███   ███ ");
	puts("  ███        ███     ███ ███   ███ ");
	puts("  ███        ███ ▄█▄ ███ ███   ███ ");
	puts(" ▄████▀       ▀███▀███▀   ▀█   █▀  \n");
}

void intro(){
	puts("INTRO:\n");

	puts("Welcome to my pwn walkthrough program.");
	puts("I hope to make pwn a little more approachable, so this problem will guide you in basic rop and format string.\n");
}

void info(){
	puts("INFO:\n");

	puts("To start out, to run this program, you will need to use some sort of linux distribution.");
	puts("If you are on windows, you can use wsl or vmware, I personally use vmware.");
	puts("To use vmware, you need to search for some linux distribution image online and follow instructions on how to set up the vm.\n");

	puts("Once you have that set up, you will want to use a python script with the pwntools library to create an exploit.");
	puts("You can read the documentation at https://docs.pwntools.com/en/stable/about.html.\n");

	puts("You may also want to use a command called checksec to see what conditions the elf binary has.\n");

	puts("Also, though you won't necessarily need it for this problem, you will likely use gdb a lot.");
	puts("Using an extension to visualize stack, registers, and memory data can be very helpful.");
	puts("I reccomend gdb peda, which you can read about at https://github.com/longld/peda.\n");

	puts("Similarly, though you won't need it for this program, a program called Ghidra is very important in both pwn and rev.");
	puts("It disassembles elf binaries so you can read the source code even when it is not given.");
	puts("You can download it at https://ghidra-sre.org.\n");

	puts("Now to get started!\n");
}

void dashdiv(){
	puts("- - - - - - - - - - - - - - - - - - - - - - -");
}

void stkstrt(){
	dashdiv();
	puts("- - - - - - - - - - Stack - - - - - - - - - -");
	dashdiv();
}

void stk(long *buf, int idx, char *mes){
	printf("%04d| 0x%llx -> %016llx %s\n", 8 * idx, &buf[idx], buf[idx], mes);
}

void stkend(){
	puts("...");
	dashdiv();
	puts("- - - - - - - - - End stack - - - - - - - - -");
	dashdiv();
	puts("");
}

void rop(){
	char buf[0x40];
	
	puts("ROP:\n");

	puts("\"Roppity hoppity, this is now my property.\"\n");

	puts("In rop, you want to take control of the program by overwriting the return address on the stack.\n");

	printf("First, here is the canary value (what is canary explained later): 0x%llx\n", ((long *)buf)[0x9]);
	puts("Now, input something into the char buf array, and I will show you what that looks like on the stack.");

	gets(buf); //here is the overflow vuln, rest is info
	puts("");

	stkstrt();
	
	stk(buf, 0x0, "(buf strt)");
	for(int i = 0x1; i < 0x7; i++) stk(buf, i, "");
	stk(buf, 0x7, "(buf end)");
	
	stk(buf, 0x8, "");
	stk(buf, 0x9, "(canary)");
	stk(buf, 0xa, "(rop func base ptr)");
	stk(buf, 0xb, "(rop func return ptr)");
	stk(buf, 0xc, "(main func base ptr)");
	stk(buf, 0xd, "(main func return ptr)");

	stk(buf, 0xe, "(stack continues below with stuff we don't care abt)");
	for(int i = 0xf; i < 0x18; i++) stk(buf, i, "");

	stkend();

	puts("As you can see, the stack contains many bits of information in a specific layout, so I will attempt to explain it.\n");

	puts("First off, local variables for the currently executing function are held at the top of the stack");
	puts("This is why you see the char buf array at the top of the stack.");
	puts("Variables that aren't initialized also contain the values held in the stack previously.");
	puts("This is why the buf array may contain some random values after the input string.");
	puts("However, the end of the inputted string is signified by a null byte placed by the gets function.\n");

	puts("After the buffer array, you can see something called a canary.");
	puts("This is a security protection against stack overflows, but it is only effective assuming the user doesn't know the canary value.");
	puts("It is a random value that is tested if it changed when a function returns.");
	puts("Not all binaries have a canary, you can find out using the checksec command mentioned in the info section.");
	puts("Probably most rop problems in ctf pwn do not use a canary, but I put one in here for educational purposes.\n");

	puts("Next, the stack contains the base pointer for the rop function.");
	puts("This signifies where the stack frame will be when the current function returns.");
	puts("This is necessary because the stack needs to point back to the local variables and return address of the function that called it.\n");

	puts("Now, we finally have the return address for the rop function.");
	puts("The return address points to where the code should continue running from after the function finishes.");
	puts("In this case, it points to code in the main function right after where the rop function is called.");
	puts("This is the value on the stack you want to overwrite to change the program to run whatever code you want to call next.\n");

	puts("Lastly, you can see the base pointer and return address of the main function as well.");
       	puts("Once the rop function returns back to main, these values will be back at the top of the stack.");
	puts("After that the stack just has more local environment data that goes on for a while.\n");

	dashdiv();

	puts("\nYou now hopefully realize the general idea on how to rop to control the next function called.");
	puts("You need to input some amount of characters that reach up to the return address and correspond to the address you want to call.");
       	puts("You also need to make sure to input characters that can correspond to the same value as the canary so it does not change value.\n");

	puts("However, you may be wondering how you are able to read past the buf array memory.");
 	puts("Well, the function gets is quite insecure, so it will actually read as long of a string as you input, even if it is longer than the memory region it is being inputted into.");
	puts("This means if you just put a long enough string you can write past the buffer array and onto other stack values.");
	puts("You can test this by typing a bunch of a's to overwrite the canary and see a message pop up stating there has been stack smashing detected.\n");

	dashdiv();

	puts("\nWe will now use the pwntools python library to create the carefully crafted string perform the rop.");
	puts("First off, the binary does not used randomized addresses, meaning we can find the address ahead of time.");
	puts("We want to call the fmtstr function, and you can find the address of that function with this python code:");
	puts(">>> e = ELF('./walkthrough')");
	puts(">>> print(hex(e.sym['fmtstr'])\n");

	puts("Now, to write an address as a string, you need to understand how memory holds numbers.");
	puts("Most memory stores numbers in something called reverse endian order, where the lowest byte goes at the earliest address.");
	puts("That means for example, the number 0x69420 would look like the string '\\x20\\x94\\x06'");
	puts("Luckily, pwntools also has a function to automatically convert a hex value into a reverse endian string, like this:");
	puts(">>> print(p64(0x69420))\n");

	puts("Finally, to communicate interact with a program, you can use these code snippets:");
	puts(">>> p = process('./walkthrough') #use this one to test locally");	
	puts(">>> p = remote('netcat.address', [port num]) #use this one to connect over netcat");
	puts(">>> p.sendline('String to send')");
	puts(">>> output_of_program = p.recv(256)");
	puts(">>> output_line = p.recvline()");
	puts(">>> output_until = p.recvuntil('input: ')");
	puts(">>> p.interactive() #allow user to input to program directly\n");

	dashdiv();

	puts("\nNow, to finally put this information all together, you will need to write something like this:");
	puts(">>> from pwn import *");
	puts(">>> e = ELF('./walkthrough')");
	puts(">>> p = process(e.path)");
	puts(">>> p.recvuntil('later): ')");
	puts(">>> canary = int(p.recvline(keepends = False), 16) #keepends = False drop the newline character");
	puts(">>> p.sendline(b'a' * x + p64(canary) + b'a' * y + p64(e.sym['fmtstr'] + 1)) #figure out what x and y values should be");
	puts("In this particular problem, notice you need the '+ 1' added fmtstr adr, which you won't normally need.");
	puts("This is due to future scanf calls needing a valid rbp value and this magically fixes it.\n");

	puts("Also, you may find the following commands useful, though not necessary for an exploit:");
	puts(">>> log.info('This func logs info to your terminal, for example the canary: ' + hex(canary))");
	puts(">>> gdb.attach(p) #open a terminal with gdb containing the current state of your program\n");

	puts("Lastly, Pwntools also has a built in tool for calling complicated chains of multiple functions with parameters.");
	puts("You can read about it at https://docs.pwntools.com/en/stable/rop/rop.html, but it is not very useful for this problem.\n");

	puts("I hope you figured it out!\n");
}

void fmtstr(){
	long num[0x8];
	char buf[0x20];
	num[0x0] = 0x31415926535;
	num[0x1] = 0x696969696969;
	num[0x2] = 0x420420420420;
	num[0x3] = 0x0;
	num[0x4] = 0x0;
	num[0x5] = 0xdeadbeef;
	num[0x6] = 0x133713371337;
	num[0x7] = 0x123456789abc;

	divide();

	puts("FORMAT STRING:\n");

	puts("\"A function's greatest strength may also be its greatest weakness.\" - Sun Tzu\n");

	puts("Nice job with the rop, looks like you made it here!\n");

	puts("You are going to have to guess a random number correctly.");
	puts("However, I will let you input a string into a buf array first. (using a more secure method without overflow)");
       	puts("I will then pass that string in printf giving you a format string vulnrability that should allow you to leak the number.");
	puts("The number will be on the num array located on the stack.");
	puts("Before I set that number, I will show you the stack.\n");

	stkstrt();

	stk(num, 0x0, "(num start)");
	for(int i = 0x1; i < 0x3; i++) stk(num, i, "");
	stk(num, 0x3, "(where guess value will be)");
	stk(num, 0x4, "(where random value will be)");
	for(int i = 0x5; i < 0x7; i++) stk(num, i, "");
	stk(num, 0x7, "(num end)");

	stk(num, 0x8, "(buf start)");
	for(int i = 0x9; i < 0xb; i++) stk(num, i, "");
	stk(num, 0xb, "(buf end)");

	stk(num, 0xc, "");
	stk(num, 0xd, "(canary)");
	stk(num, 0xe, "(fmtstr base ptr, messed up from rop)");
	stk(num, 0xf, "(fmtstr return adr, useless since exit func called at end of this function)");
	stk(num, 0x10, "(stuff below is useless now)");
	for(int i = 0x11; i < 0x18; i++) stk(num, i, "");

	stkend();

	puts("I will now set the random number.\n");

	num[0x4] = rand();

	dashdiv();

	puts("\nNow, you may be wondering what a format string vulnerability is.");
	puts("Well, you may be familiar with the function printf, which uses a string with formatters to create a specific output.");
	puts("See https://en.wikipedia.org/wiki/Printf_format_string for more info.\n");

	puts("When user input is passed in the first parameter where constant formatters are supposed to go this is called a format string vulnerability.");
	puts("Ie the code 'printf(\"\%s\", buf)' is correct, but 'printf(buf)' is vulnerable.");
	puts("With a carefully crafted input, a user can leak values on the stack and even write to addresses on the stack.");
	puts("You will only need to leak a value for this problem though.\n");

	puts("To see what I mean, I encourage you to experiment with the input '\%[number]$llx', where you decide the number.");
	puts("I think you should be able to figure out the rest from here. :pray:\n");

	dashdiv();

	puts("\nInput the string that will be passed into printf.");
	scanf("%31s", buf);

	puts("\nThe printf result is:");
	printf(buf); //here is format string vuln, rest is info
	puts("\n");

	dashdiv();

	puts("\nNow input the value you're guessing.");
	scanf("%lld", &num[0x3]);

	puts("\nNow testing if random and guess values are equal.\n");

	dashdiv();
	puts("");

	if(num[0x3] == num[0x4]){
		puts("You beat rng!\n");

		FILE *f = fopen("flag.txt","r");
		if(f == NULL){
			puts("If you are running locally, you need to create a file called 'flag.txt' in the running progam's directory.");
			puts("Otherwise, something is wrong. Please contact the author on discord.");
			exit(1);
		}

		fgets(buf, 0x20, f);

		puts("After all that program manipulation, here's the flag:");
		puts(buf);
	}else{
		puts("You failed baka.");
	}

	exit(0);
}

void outro(){
	puts("OUTRO:\n");

	puts("Whoops, looks like you didn't rop anywhere.");
	puts("Make sure to overflow all the way to the return address to control what function is called.");
}

int main(){
        setbuf(stdout, 0x0);
        setbuf(stderr, 0x0);
	srand(time(0));

	ascii();

	divide();

	intro();

	divide();

	info();

	divide();
	
	rop();

	divide();

	outro();

        return 0;
}
