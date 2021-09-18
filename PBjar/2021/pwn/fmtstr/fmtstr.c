#include <stdio.h>
#include <stdlib.h>

void divide(){
        puts("---------------------------------------------------------------------------------------\n");
}

void asciiart(){
	puts("/$$$$$$$$              /$$      /$$$$$$   /$$              ");
	puts("| $$_____/             | $$     /$$__  $$ | $$              ");
	puts("| $$    /$$$$$$/$$$$  /$$$$$$  | $$  \\__//$$$$$$    /$$$$$$ ");
	puts("| $$$$$| $$_  $$_  $$|_  $$_/  |  $$$$$$|_  $$_/   /$$__  $$");
	puts("| $$__/| $$ \\ $$ \\ $$  | $$     \\____  $$ | $$    | $$  \\__/");
	puts("| $$   | $$ | $$ | $$  | $$ /$$ /$$  \\ $$ | $$ /$$| $$      ");
	puts("| $$   | $$ | $$ | $$  |  $$$$/|  $$$$$$/ |  $$$$/| $$      ");
	puts("|__/   |__/ |__/ |__/   \\___/   \\______/   \\___/  |__/\n");
}

void intro(){
	puts("INTRO:\n");

	puts("Have you used printf in C?\n");

	puts("When you use it, it is important to format data to output correctly, especially when ouputting user input.\n");

	puts("When done incorrectly, printf becomes a powerful tool to the user. :sunglasses:\n");
}

void explain_fmtstr(){
	puts("EXPLAIN FMTSTR:\n");

	puts("First off, if you don't already, you need to understand formatting for printf.\n");

	puts("When using printf, the code should look something like:");
	puts("printf(\"[constant string with formatters]\", [input to format 1], [input to format 2], etc...);\n");

	puts("There are many formatters, for different types of input.\n");

	puts("Here are some:\n");

	puts("\%s: string");
	puts("\%c: character");
	puts("\%d: signed integer");
	puts("\%x: hex integer");
	puts("\%p: address");
	puts("\%n: print nothing but write number of previously printed (not number of input) characters to input address (why does this even exist?)\n");

	puts("An example of how this would be used is the following:");
	puts("printf(\"Best girl is \%s \%d, duh!\\n\", \"Amy\", 2);\n");

	puts("This would output:");
	printf("Best girl is %s %d, duh!\n", "Amy", 2);

	puts("");

	puts("However, the formatters can have much more specifications.\n");

	puts("A more complete template to formatters would be:");
	puts("\%[parameter][flags][width][.precision][length]type\n");

	puts("The most important things are:\n");	

	puts("Paramater - by using 'n$' between the '\%' and type, you can choose which input position the format string takes the value from.");
	puts("Width - sets the minimum amount of characters to be printed, will print spaces unless character specified before width");
	puts("Length - Can add modifiers before type such as to change the size of the input, such as 'hh' to take a byte, or 'll' to take a long long\n");

	puts("Here's one more example with the new format options:");
	puts("printf(\"\%3$s, please go on a date with me in \%6$020lld days!\\n\", \"Amy Wan\", \"Amy Tu\", \"Yusa Ko\", 3, 21, 694203141592653);\n");

	puts("This would output:");
	printf("%3$s, please go on a date with me in %6$020lld days!\n", "Amy Wan", "Amy Tu", "Yusa Ko", 3, 21, 694203141592653);

	puts("");

	puts("You can find more details on wikipedia.\n");
}

void explain_exploit(){
	puts("EXPLAIN EXPLOIT:\n");

	puts("All that format stuff is great and all, but how would it possibly be used in an exploit?\n");

	puts("Well, if the programmer formats the output correctly, it can't. :weary:\n");

	puts("However, what if you, as the user, were able to control the first parameter that uses the formatters? :think:\n");

	puts("A common beginner mistake is to write code like 'printf(buf);', where buf is a string the user can write to.\n");

	puts("When this is the case, whatever formatters you input to buf will still be used! :eyes:\n");

	puts("You may be thinking, 'what does the formatters do if there aren't any other parameters to use tho?'\n");

	puts("Well the magical thing is, printf's inputs are on the stack, so you are able to print and modify stack addresses as if they are inputs!\n");

	puts("In the exploit, try typing '\%p \%p \%p \%p \%p \%p \%p', and you will see that you are in fact leaking addresses.\n");

	puts("Even more lucky for you, libc addresses seem to always find their way onto the stack!\n");

	puts("In gdb peda, an easy way to view the stack is just the command 'stack [number addreses to output]'.\n");

	puts("Also remember that weird '\%n' formatter?\n");

	puts("Well, because it can write to an address on the stack, if you are able to place an address on the stack you want to write to, you can than write to it!\n");

	puts("Luckily, it is **almost always** the case the input string is located on the stack, so you can just write addresses on the input string.\n");

	puts("What if you overwrote a got address causing a function to call something other than the intended libc address it's supposed too? :eyes:\n");

	puts("And a tip, to print some number of chars that are used as the '\%n' write value, just type '\%[number chars]c'\n");

	puts("Another tip, rather than writing all characters at once (where you'd have to print a ton of characters), split the write into bytes or shorts with the size length modifier.\n");

	puts("Overall, your goal should be:\n");

	puts("1) leak libc address from stack.");
	puts("2) Overwrite a function got with system so you can put '/bin/sh' into it.");
	puts("3) Put '/bin/sh' into that function\n");

	puts("Don't forget the input position modifier for formatters, it makes it easier to get the stack offsets you want.\n");

	puts("Btw, I heard pwntools can make writes with printf way easier than by hand (specifically the fmtstr_payload function).\n");

	puts("To use it, make sure you set the pwntools context arch correctly.\n");
}

void resources(){
	puts("RESOURCES:\n");

	puts("I know, I'm too nice, giving you even more help.\n");

	puts("Here are a few maybe helpful links:\n");

	puts("Video tutorial (and great channel): https://www.youtube.com/watch?v=t1LH9D5cuK4");
	puts("Wikipedia printf formatters: https://en.wikipedia.org/wiki/Printf_format_string");
	puts("Pwntools fmtstr: https://docs.pwntools.com/en/stable/fmtstr.html\n");
}

void learn(){
	char buf[32];

	puts("WANT TO LEARN:\n");

	puts("Before we start, would you like to learn about format string exploits?[y/N] (also, I fixed the overflow here :clown:)");

	fgets(buf, 32, stdin);

	puts("");

	if(buf[0] == 'y' || buf[0] == 'Y'){
		divide();

		explain_fmtstr();

		divide();

		explain_exploit();

		divide();

		resources();
	}else{
		puts("I see, you must be a natural!\n");
	}
}

void vuln(){
	char buf[128];

	puts("EXPLOIT:\n");

	puts("Here we go, I'll be nice and read three inputs, and all three will be outputted with printf as its first paramter.\n");

	puts("However, no overflows, I won't take more than 128 characters at a time. :pensive:\n");

	puts("Give me your first input:");

	fgets(buf, sizeof(buf), stdin);

	printf(buf);

	puts("");

	puts("Nice, now give me your second input:");

	fgets(buf, sizeof(buf), stdin);	

	printf(buf);

	puts("");

	puts("Alright, one last input:");

	fgets(buf, sizeof(buf), stdin);	

	printf(buf);

	puts("");
}

void farewell(){
	puts("FAREWELL:\n");

	puts("Hopefully something worked right!\n");

	puts("Adios!\n");
}

int main(){
	setbuf(stdout, 0x0);
        setbuf(stderr, 0x0);

	asciiart();

	divide();

	intro();
	
	divide();

	learn();

	divide();

	vuln();

	divide();

	farewell();

	return 0;
}
