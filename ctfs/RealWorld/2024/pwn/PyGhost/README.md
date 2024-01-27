Pwn, Misc, demo, difficulty: Schrödinger

This is an LPE(Local Privilege Escalation) challenge. Your task is to pop a highly-privileged(nt authority\system) cmd.exe as a low-privileged user. Follow these steps to deploy the challenge locally:

    download and install the virtual machine from: https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/
    execute the installer (installer.exe in the attachment) as Administrator
    the installer will set up the vulnerable component. You can then attempt to find the vulnerability and exploit it

Notes about the demo:

    Send your exploit archive file to demo@realworldctf.com and DM @M4x on Discord when you're ready. Meanwhile, the email should also contains your team name and team token
    You can choose to demo your exploit publicly or privately, according to your preference. If you choose to demo publicly, the entire process will be visible to everyone, so remember to remove sensitive information. If you choose to demo privately, we will set up a private discord channel that only includes the admin and your team members
    Our demo VM is slightly configured, including:
    a. Windows Defender is disabled. You don't have to contend with it.
    b. A standard user(not in the Administrator group, with the username being ctf) is created for demo purposes. We will run your exploit in the context of the standard user.
    If your exploit needs multiple steps, please batch them in a single file. We will only execute one of your files and then wait for the result without more user interaction

I will not accept more than 3 emails per team. If you really need more, you will need to explain to me in detail why you messed up your first 3 tries and convince me that you deserve a 4th chance.
The running time for each try cannot exceed 3 minutes.

I will reward you with the flag if the highly-privileged cmd.exe pops up.
