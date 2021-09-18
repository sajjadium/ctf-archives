#include <stdio.h>

void divide(){
	puts("---------------------------------------------------------------------------------------\n");
}

void asciiart(){
	puts("__________        __  ________ .____    ._____. ");
	puts("\\______   \\ _____/  |_\\_____  \\|    |   |__\\_ |_");
	puts(" |       _// __ \\   __\\/  ____/|    |   |  || __ \\_/ ___\\ ");
	puts(" |    |   \\  ___/|  | /       \\|    |___|  || \\_\\ \\  \\___ ");
	puts(" |____|_  /\\___  >__| \\_______ \\_______ \\__||___  /\\___  >");
	puts("        \\/     \\/             \\/       \\/       \\/     \\/ \n");

}

void intro(){
	puts("INTRO: \n");

	puts("This is a classic ret2libc task, and understanding it is essential to solving all pwn problems this contest.\n");

	puts("Essentially, a buffer overflow is more powerful than you might have realized!\n");

	puts("With just a single buffer overflow, you can get a shell on a remote server, even without a win function! :eyes:\n");
}

void setup(){
	puts("SETUP: \n");

	puts("To try this exploit on your computer, you need to use a tool called patchelf to link the binary with the correct libc and dynamic linker version provided.\n");

	puts("To get patchelf, type 'sudo apt-get install patchelf' in your terminal.\n");

	puts("To use it, type 'patchelf --set-interpreter ./ld-ret2libc.so --add-needed ./libc-ret2libc.so ./ret2libc'.\n");

	puts("In general, you will need to do this for every problem where your exploit uses the libc.\n");
}

void explain_pltgot(){
	puts("ABOUT PLT AND GOT: \n");

	puts("Hopefully, you remember how to use an overflow to rop to a win function.\n");

	puts("Well that idea can be expanded on further, by calling functions in both the binary and libc.\n");

	puts("When you use library calls, have you ever wondered how that works? :think:\n");

	puts("The binary will internally have some links to the functions in libc, that it uses to call upon.\n");

	puts("These functions are known as plt functions, as they are located in the .plt section of the binary.\n");

	puts("For example, in this binary, the 'puts' and 'gets' function will be located in the plt.\n");

	puts("However, the actual libc addresses the plt functions use to call are located in a seperated section, called the .got section.\n");

	puts("You can find these address offsets for a binary in pwntools using the ELF module, or you can also use objdump/readelf.\n");
}

void explain_rop(){
	puts("HOW TO USE PLT AND GOT TO CALL SYSTEM: \n");

	puts("Okay, so how does this help?\n");

	puts("Well, since system is in libc that the program uses, what is stopping us from just calling that (why do you think it's called ret2libc)? :eyes:\n");

	puts("But wait, libc addresses are randomized, how do we know the libc base address?\n");

	puts("If only there were a plt function you could call with rop that could print a libc address from the got table...\n");

	puts("Also, even with one overflow, what if could you call a function to get back to another overflow again? :think:\n");

	puts("One more thing, to load addresses to functions in x86_64 binaries, you need to use something called gadgets.\n");

	puts("Functions with a single variable are loaded with the 'pop rdi ; ret' gadget, which then puts the following address on the stack into the rdi register.\n");

	puts("You rop to them just like anything else, by putting their address after the overflow.\n");

	puts("You can find their addresses with the tool ROPgadget.\n");
}

void resources(){
	puts("RESOURCES: \n");

	puts("Still confused?\n");

	puts("Luckily, since this is likely your first ret2libc, I'll give you some links to make it easy. :sunglasses:\n");

	puts("Hopefully these will help you understand:\n");

	puts("Article tutorial: https://pwning.tech/2019/07/29/ret2libc-pwntools/");
	puts("Similar problem writeup (the code will probably help a lot): https://github.com/datajerk/ctf-write-ups/blob/master/redpwnctf2020/the-library/README.md");
	puts("Elf module pwntools: https://docs.pwntools.com/en/2.2.0/elf.html");
	puts("ROPgadget download: https://github.com/JonathanSalwan/ROPgadget"); 
	puts("Also in general, make sure you use 'peda' extenion for gdb: https://github.com/longld/peda");
	puts("And this may make life much easier: https://docs.pwntools.com/en/stable/rop/rop.html\n");

	puts("And if that's not enough, remember this is a classic problem, so there should be tons of similar writeups you can google!\n");
}

void learn(){
	char buf[32];

	puts("WANT TO LEARN: \n");

	puts("Before we start, would you like to learn about ret2libc?[y/N]");

	gets(buf);

	puts("");

	if(buf[0] == 'y' || buf[0] == 'Y'){
		divide();

		explain_pltgot();

		divide();

		explain_rop();

		divide();

		resources();
	}else{
		puts("I see, you must be a natural!\n");
	}
}

void farewell(){
	puts("FAREWELL: \n");

	puts("Well did it work? Wait, did it even start?\n");

	puts("(If you think it should work and it didn't, try ropping to 'ret' gadget [pop_rdi + 1] first to align stack.)\n");

	puts("Adios!\n");
}

int main(){
	setbuf(stdout, 0);
	setbuf(stderr, 0);

	asciiart();

	divide();

	intro();

	divide();

	setup();

	divide();

	learn();

	divide();

	farewell();

	return 0;
}
