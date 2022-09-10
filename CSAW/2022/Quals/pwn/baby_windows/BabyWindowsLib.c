#include "BabyWindowsLib.h"
#include <stdio.h>
#include <windows.h>
#include <synchapi.h>

void PrintCSAWBanner(){
    printf(" #####   #####     #    #     #     #####    ###    #####   ##### \n");
    printf("#     # #     #   # #   #  #  #    #     #  #   #  #     # #     #\n");
    printf("#       #        #   #  #  #  #          # #     #       #       #\n");
    printf("#        #####  #     # #  #  #     #####  #     #  #####   ##### \n");
    printf("#             # ####### #  #  #    #       #     # #       #      \n");
    printf("#     # #     # #     # #  #  #    #        #   #  #       #      \n");
    printf(" #####   #####  #     #  ## ##     #######   ###   ####### #######\n");
    return;
}

void PrintOS(){
    printf("__        ___           _                     ____   ___  _  ___    ____                               \n");
    printf("\\ \\      / (_)_ __   __| | _____      _____  |___ \\ / _ \\/ |/ _ \\  / ___|  ___ _ ____   _____ _ __     \n");
    printf(" \\ \\ /\\ / /| | '_ \\ / _` |/ _ \\ \\ /\\ / / __|   __) | | | | | (_) | \\___ \\ / _ \\ '__\\ \\ / / _ \\ '__|    \n");
    printf("  \\ V  V / | | | | | (_| | (_) \\ V  V /\\__ \\  / __/| |_| | |\\__, |  ___) |  __/ |   \\ V /  __/ |       \n");
    printf("   \\_/\\_/  |_|_| |_|\\__,_|\\___/ \\_/\\_/ |___/ |_____|\\___/|_|  /_/  |____/ \\___|_|    \\_/ \\___|_|       \n");   
}

void Pontificate(){
    printf("   An interesting fact about running Windows Docker containers:\n");
    printf("it's possible to run 64-bit applications in NanoServer,\n");
    printf("with a footprint of a few hundred megabytes. NanoServer doesn't\n");
    printf("run 32-bit applications. It's possible, however, to force\n");
    printf("Nanoserver to run such applications by figuring out what DLLs\n");
    printf("are missing to do so using Process Monitor and then copying\n");
    printf("those DLLs into the Docker container. But it's not really a \n");
    printf("sustainable way to deploy 32-bit Windows pwnables in CTFs in\n");
    printf("the long run, and additionally running shellcode in such a \n");
    printf("manner will look for cmd.exe in the wrong location. It's\n");
    printf("unlikely that Microsoft will support 32-bit applications in \n");
    printf("Nanoserver anytime soon -- there's no market for it -- so we\n");
    printf("are likely stuck with large Docker footprints to pwn 32-bit \n");
    printf("applications in CTFs for the forseeable future. If you come up \n");
    printf("with a workaround, let the community know!\n");
    fflush(stdout);
}

void Pwn(){
    // Give shell
    WinExec("cmd.exe", SW_SHOWDEFAULT);
    // The above call is asynchronous, unlike system("/bin/sh") in Linux.
    // Many Windows exploits deal with this by creating a new socket and execute cmd.exe in a new process
    // listening on that socket. Then the shellcode gracefully exits the original program. 
    // This challenge is running in a Docker container with one exposed port, so that's not an option.
    // So we're going to sleep for two minutes and then exit, giving you time to spawn a shell and get the flag.
    Sleep(120000);
    ExitProcess(0);
}

//This DLL was compiled as follows. We're disabling a bunch of security features as this is a beginning Windows exploitation challenge.
//C:\msys64\mingw32\bin\gcc.exe -m32 -DCSAW_EXPORTS -shared -Wl,--image-base=0x[REDACTED],--disable-dynamicbase,--disable-nxcompat,--disable-reloc-section -o BabyWindowsLib.dll BabyWindowsLib.c
