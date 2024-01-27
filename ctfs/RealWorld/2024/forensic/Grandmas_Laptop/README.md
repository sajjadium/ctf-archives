Forensics, difficulty: Normal

    Unfortunately, my grandma has passed away recently. The photos in her laptop
    are the only memory of her that I have. However, I could not remember the
    password of her laptop. The photos are protected by BitLocker and cannot be
    read out directly from the disk. I am trying to restore the photos. I really
    need your help.


# Grandma's Laptop


## Goal

Bypass BitLocker on SecureBoot-enabled x86-64 PC


## Setup

OS: Windows 11 23H2 22631.3007

> manage-bde.exe -protectors C: -get
BitLocker Drive Encryption: Configuration Tool version 10.0.22621
Copyright (C) 2013 Microsoft Corporation. All rights reserved.

Volume C: []
All Key Protectors

    TPM:
      ID: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX}
      PCR Validation Profile:
        7, 11
        (Uses Secure Boot for integrity validation)

    Numerical Password:
      ID: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX}
      Password:
        XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX


## Web Interface (when you're ready to capture the flag)

### Login

Visit https://47.88.103.9:1337/.
Username: team
Password: <YOUR_TEAM_TOKEN>

### USB Flash Drive

Each team owns 2 USB Flash Drives that can be attached to grandma's laptop.
You can upload maximum 8 GiB of raw disk image for each drive.
You can choose whether you want to attach a drive before powering up VM.

### Console (aka. VM)

Due to limited hardware capacity, console access is time-limited and provided
upon request. Each team shares a single console.

After click `Request console access` button, you have 15 minutes to play with
it. The VM's state is persisted across power cycles, and purged when 15 minutes
expire.

After click `Power Up` button, there will be a VNC console pop-up. Where you
have access to vga / keyboard / mouse / power-controls.

### Network

A single NIC is always attached to the VM. After VM power-up, the homepage
will show `NIC URL`. A client software, which pumps frames between remote
WebSocket and local TAP interface, is provided in the challenge attachment.

For Linux:

./nic-client-linux-amd64 -persist -url wss://47.88.103.9:1337/nic/XXXXXXXXXXXX

For Windows:

nic-client-windows-amd64.exe -url wss://47.88.103.9:1337/nic/XXXXXXXXXXXX

The source code of the client software is also provided AS IS.


## Q & A

### How to access boot menu?

Reset the VM via VNC and press F2/ESC hard.

### Where is the flag?

C:\flag.txt
