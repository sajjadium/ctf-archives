package main

import (
    "os"
    "fmt"
    "syscall"
    b64 "encoding/base64"
    libseccomp "github.com/seccomp/libseccomp-golang"
)


func whiteList(syscalls []string) {

    fmt.Printf("|------------------------------------------|\n")
    fmt.Printf("\033[0;33m[!] Sandboxing all syscalls\033[0m\n")

    filter, err := libseccomp.NewFilter(libseccomp.ActErrno.SetReturnCode(int16(syscall.EPERM)))
    if err != nil {
        fmt.Printf("Error creating filter: %s\n", err)
    }
    for _, element := range syscalls {
        fmt.Printf("[+] Whitelisting: %s\n", element /*"*****"*/)
        syscallID, err := libseccomp.GetSyscallFromName(element)
        if err != nil {
            panic(err)
        }
        filter.AddRule(syscallID, libseccomp.ActAllow)
    }
    filter.Load()
    fmt.Printf("\n|------------------------------------------|\n")
}

func main() {

    /* get parameter from command line and decode to base64, then write it to disk */
    if len(os.Args) != 2 {
       fmt.Printf( "[!] ERROR, argument missing\n\033[1;31mUse 'http://ip:port/?arg=<base64 encoded code>' to run your code inside the sandbox\033[0m\n\n")
       return
    }

    sDec, _ := b64.StdEncoding.DecodeString(os.Args[1])

    file, err := os.Create("/tmp/your_code")
    if err != nil {
	panic(err)
    }
    _, errW := file.Write(sDec)
    if errW != nil {
	panic(errW)
    }

    // Change permissions Linux.
    err = os.Chmod("/tmp/your_code", 0777)
    if err != nil {
	panic(err)
    }
    file.Close()

    //===== S A N D B O X     S T A R T S =====
    var syscalls = []string{
    "mmap", "mprotect", "write", "open", "close", "fstat",
    "execve", "arch_prctl", "stat", "futex", "exit_group" }

    whiteList(syscalls)

    fmt.Printf( "\n[+] Now decoding your code...\n")
    fmt.Printf( "[+] Running your code...\n\n\033[1;33mSTDOUT:\n=======\033[0m\n")

    err2 := syscall.Exec("/tmp/your_code", nil, nil)
    if err2 != nil {
        fmt.Printf( "[-] Error encountered while running your code!\n%s\n", err2)
    }

    fmt.Printf("\n\n\033[1;32m|-------------END OF EXECUTION---------------|\033[0m\n")

    // infinite loop
    for {
    }
}

