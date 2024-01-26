Web, Pwn, difficulty:Schrödinger

    You sent a nightmail in the moon's pale glare, Then in my slumber, nightmares came to snare.

About the challenge:

    Environment setup: You can use the software installation package provided in the attachment to build a local environment for test. You can follow the default steps during installation, except for the Set up encryption step, you should choose Continue without encryption option.

    Find the vulnerability: Try to find a Remote Code Execution (RCE) vulnerability in eM Client installed in Windows, the vulnerability should be triggered when the victim clicks the malicious email sent by you.

    Capture the flag: After your exploit successfully works in your local environment, you can connect to nc 47.89.252.163:1337 to apply for your team's independent vm environment and then try to obtain the flag.

About the vm:

    OS: Windows Server 2022 x64
    Software version: eM Client v9.2.2157
    Path to flag: C:\flag
    After the vm starts, an automated script will simulate logging into eM Client with the victim email address. After waiting for 5 minutes, it will click on the most recent email in the inbox.
    The vm will be destroyed after 15 minutes.
    If you are sure that your exploit can work locally but keeps failing in the remote vm environment, please contact me (@voidfyoo) on discord channel.

https://rwctf.oss-accelerate.aliyuncs.com/emclient-568e1a4c9ac16bda48f33ed1d1d325b1.zip
