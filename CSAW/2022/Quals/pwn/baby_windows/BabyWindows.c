#include <windows.h>
#include <stdio.h>
#include "BabyWindowsLib.h"
#include <winbase.h>
#include <threadpoollegacyapiset.h>

HANDLE gDoneEvent;
HANDLE hTimerQueue;

void Vuln(){
    char buf[500];
    //puts("   Here's an introductory Windows challenge! This is best for people who have done some Linux pwning before but not with Windows.");
    //puts("Normally the goal for a challenge is to make the tooling super easy so that you can get down to learning exploitation techniques.");
    //puts("Now in this case, there's a learning curve with tooling when you start pwning Windows for the first time, it's unavoidable. So the");
    //puts("vulnerability is straightforward to find, but exploiting it will take some practice and some tool setup. If you're new to Windows");
    //puts("pwning, expect to spend a lot of time messing around with Windows debuggers and learning about shellcode for the second challenge.\n\n");

    puts("Here's a baby Windows challenge! We've got Windows running in a Windows Docker container. Some things for you to know:\n");

    puts("1. There's a steeper learning curve for exploiting Windows vs. Linux binaries, but it's worth it because a huge portion of the market is Windows,");
    puts("so the attackers are going after Windows and a ton of jobs involve defending Windows.\n");

    puts("2. If you're new to Windows exploitation, you'll probably spend the majority of your time for this challenge figuring out tooling. Learning");
    puts("the tooling is meant to be part of the challenge.\n");

    puts("3. Our challenge is running in a Windows Server Core 2019 Docker container on a Windows Server 2019 Windows instance. Windows Server Core 2019");
    puts("has a big footprint, about 5GB. Compare that to most Linux containers which are tiny in comparison. But we think it's worth the tradeoff,"); 
    puts("so we can give you a 32-bit binary to pwn and you will have more ways to debug your exploit. We think that makes sense as many people will be");
    puts("pwning their first Windows binary with this challenge.\n");

    puts("4. Learning to pwn Windows isn't free, but the cost is manageable. One fast way to get started is to set up an AWS EC2 instance running");
    puts("Windows Server 2019 with Containers. That will give you immediate access to Docker for Windows, and there's a free tier option (t2.micro)."); 
    puts("Note that if you are starting this challenge late in the competition, you might consider using a t2.medium instance and going for the second"); 
    puts("CPU core. It's still only about $0.016 / hour. Do remember to terminate your instance after the competition.\n");

    puts("5. If you're in a part of the world without access to AWS or want to do everything locally, running our Windows Docker container");
    puts("locally may be your biggest pain point. In a real pinch, you can try pwning this challenge without running the Docker container at all.");
    puts("Keep in mind that you're better off in the long run being able to test and debug your exploits against the challenge running in a Docker container.\n");

    puts("6. The flag is in \"C:\\chal\\flag.txt\".\n");

    puts("Good luck and welcome to Windows pwning! Did you gets all that?\n");

    printf("> ");
    fflush(stdout); 

    gets(buf);
    return;
} 

VOID CALLBACK TimerRoutine(PVOID lpParam, BOOLEAN TimerOrWaitFired){
    printf("Alarm clock triggered. Exiting to conserve resources on the server.\n");
    ExitProcess(0);
    SetEvent(gDoneEvent);
}

int RunChallenge(){
    fflush(stdout);
    printf("WELCOME TO \n\n\n");
    PrintCSAWBanner();
    printf("\n\nSTARRING");
    printf("\n\n");
    PrintOS();
    printf("\n\n");
    Vuln();
    return 0;
}

int Alarm(int timeOut){
    //Complicated routine that does the same thing as the one-line alarm(120) in Linux
    // https://docs.microsoft.com/en-us/windows/win32/sync/using-timer-queues
    HANDLE hTimer = NULL;
    hTimerQueue = NULL;
    int timerArg = 0; // Argument to the timer routime, we don't really use it but it's part of the API
    gDoneEvent = CreateEvent(NULL, TRUE, FALSE, NULL);

    if (NULL == gDoneEvent)
    {
        printf("CreateEvent failed (%d)\n", GetLastError());
        return 1;
    }

    hTimerQueue = CreateTimerQueue();
    if (NULL == hTimerQueue)
    {
        printf("CreateTimerQueue failed (%d)\n", GetLastError());
        return 2;
    }

    // Set a timer to call the timer routine in 120 seconds.
    if (!CreateTimerQueueTimer(&hTimer, hTimerQueue, (WAITORTIMERCALLBACK)TimerRoutine, &timerArg, timeOut, 0, 0)){
        printf("CreateTimerQueueTimer failed (%d)\n", GetLastError());
        return 3;
    }
    return 0;
}

int CleanUp(){
    CloseHandle(gDoneEvent);

    // Delete all timers in the timer queue.
    if (!DeleteTimerQueue(hTimerQueue))
        printf("DeleteTimerQueue failed (%d)\n", GetLastError());
}

int main(){
    Alarm(120000); // Alarm clock, timeout is in milliseconds
    RunChallenge();
    CleanUp();
    return 0;
}