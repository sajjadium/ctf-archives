This is the final boss of the Full Chain series. Enjoy!

Challenge

https://chal-the-umi.hitconctf.com:8000/

Introduction

    You need to complete wall-sina, wall-rose, and wall-maria before you begin this challenge
        Whether you choose to finish the-blade before solving this challenge is optional; you can just use the tool directly
    This is a pentest-style challenge, and there should be no additional pwnable vulnerabilities except for the ones in wall-sina, wall-rose, and wall-maria (and maybe 0days :) ).

Mindmap

    Chroot Jailbreak in Linux VM
        Covered in wall-sina
    Privilege Escalation in Linux VM
        Covered in wall-rose
    Qemu VM Escape
        Covered in wall-maria
    Seccomp Shell "Escape" → Remote Code Execution in Docker
        You can use the binary in the-blade to simplify such process
    Privilege Escalation in Docker
        Find misconfigurations in the docker environment to achieve privilege escalation. (DON'T ATTACK THE KERNEL PLEASE)
    STOP HERE! DO NOT TRY TO ESCAPE THE DOCKER OR ATTACK THE KERNEL PLEASE!

Flag location

    Somewhere in /root
