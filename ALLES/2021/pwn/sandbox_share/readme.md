# readme

## General

Steps to replicate the remote setup:

1. First run `install.sh` to build and install all required files.  
2. Afterwards, run `run.sh`.  

If you need to restart the `sandbox_share_xpc` service, run `restart_service.sh`.

## Notes

- Your exploit should take the service name from `argv[1]`



We feel like macOS is underrepresented in CTFs so here you go:

Challenge:

nc sandbox-share.allesctf.net 8090

VM Information:

~$ sw_vers
ProductName:	macOS
ProductVersion:	11.5.2
BuildVersion:	20G95

You can use this to get a local instance if you don't own a mac: https://github.com/sickcodes/Docker-OSX

Hint:

    Woah what? You can just put mach ports into xpc messages and send them to other processes O.o
    "The more you allocate, the more you can free" ~孙子
    Who needs RIP control when you can have:

typedef struct {
    uint64_t class_ptr;
    uint32_t pad[2];
    uint32_t ref_count;
    uint32_t pad1;
    mach_port_t port_name;
    uint32_t pad2;
} fake_xpc_mach_port_t;

