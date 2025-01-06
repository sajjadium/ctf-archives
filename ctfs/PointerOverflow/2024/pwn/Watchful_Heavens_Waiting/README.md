This exploit challenge was almost the 400-level challenge, but I swapped it out because I wasn't confident that it was accessible. I'm really curious to see how you do, and if it goes well I might be using a similar setup for my Software Exploit course!

Here's the premise: I'll provide you with a VM. I have created a user called 'ctf', password 'ctf'. And I have placed the flag in the root directory. All you need to do is get to it. To help you with that, this VM has a kernel module that has a couple problems. I've provided you with the source code (I have even notated the problematic statements for you) and Makefile, just so you can see how the sausage was made.

The module should load when you boot it up, but you can check if its running with lsmod | grep Exploit300-3

ISO - Source and Makefile
MD5 checksum 47DE99ECA0575016C43930791C07F483

QCOW2 Image
MD5 checksum 777B3F89959F4CC337E115F3C41C7FC8

https://uwspedu-my.sharepoint.com/:u:/g/personal/cjohnson_uwsp_edu/EZ9_AapV805DvNvpGSS_PQwBQR_OoanD21C5HcQdhBvymg?e=aRMKAH

