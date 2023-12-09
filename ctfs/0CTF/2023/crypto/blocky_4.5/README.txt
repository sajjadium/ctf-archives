## README

This task is based on the challenge `blocky-5` in pbctf 2023, which is made by @RBTree_.

Files related to this challenge:
	- `GF.py`: same as that in `blocky-5`.
	- `Cipher.py`: only line 70 and 82 are modified, from "if i < self.rnd - 1:" to "if i < self.rnd - 2:".
	- `task.py`: source code of the remote server.

To make it fair, here we also provide files related to the original challenge:
	- `./misc/blocky5.zip`: source code of `blocky-5`.
	- `./misc/discord-chat.html`: exported chat logs in the pbctf official Discord channel, where you may find the intended solution of `blocky-5`.