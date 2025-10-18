This challenge is sponsored by Binary Gecko! To qualify for a prize, solve it in a group of at most three people and submit a well-written write-up. More info and exact criteria below.

Sponsor Info
Binary Gecko Logo

Binary Gecko, which also runs Offensivecon, is a German company who conducts the most complex Vulnerability Research out there. We aim to be the best company in the world for talented security researchers with a "work hard - play hard" approach.

Have in-depth knowledge of kernels, browsers or hypervisors? Or think you are getting there? We want you in our team!

If you are interested in working with us, please reach out to us at careers@binarygecko.com

Prize Info
To qualify for the prize for this challenge, three tickets for OffensiveCon 2026, you need to:

Solve this challenge in a group of at most three people. It's fine to solve it alone, or with less than three people, but not with a group of four or more. This group can be three people out of a larger team, and you can just submit the flag as the team.
For example, three Windows-enjoying people of the 20-people FluxFingers team could work on this challenge, submit the flag as the FluxFingers team, and qualify for the challenge.
Submit a well-written write-up for the challenge via a ticket on our Discord server, mentioning the (at most) three people that collaborated on solving the challenge.
After the CTF, the best write-up will then be selected by us (FluxFingers) in collaboration with Binary Gecko, and the authors will be awarded the prize by Binary Gecko.

The actual people out of that team that solved the challenge are encouraged to go to OffensiveCon, as they will bring and earn the most value to and from the conference.

Note that if you submit a write-up with less than three people, it is up to Binary Gecko to decide whether you will get the full three tickets. However, the (at most three) people who collaborated on solving the challenge are guaranteed to receive a ticket.

Challenge Info
In this challenge, you will need to exploit CVE-2023-21688, a use-after-free vulnerability in the AlpcpCreateView function. We have ported the bug to the most recent version of Windows 11 25H2 at the time of writing. The attachment file contains the patched ntoskrnl.exe as well as the full challenge description, which contains instructions on setting up a local instance of the challenge for debugging. The VM image is linked in the README.md in the archive because of its size (~17GB). You are provided with a ynetd-like interface to the remote, where you can submit a PE file that will be executed with a Low-Privileged AppContainer (LPAC) Token. Your goal is to elevate privileges and read the flag from \\?\PHYSICALDRIVE2. Good luck!

Note: For local testing, it is recommended to connect to the VM via RDP, access is enabled with credentials Administrator:password.

Product Info
Designer: SeTcbPrivilege
