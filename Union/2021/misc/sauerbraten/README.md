We love Cube 2: Sauerbraten so much that we decided to host a server so you could enjoy some gaming during the CTF.

Become an admin of the server (>= PRIV_ADMIN) and then send getflag in the game chat to retrieve the flag.

The game running on the server is a clone of the repo at https://svn.code.sf.net/p/sauerbraten/code/. Specifically the commit r6491, which was HEAD at the time of writing. The only changes we have made are in changes.patch.

Your goal is to escalate your privileges in the game to admin. Once you are admin then you can send the string `getflag` in the game chat, and the server will respond with the flag. 

Tips:
- If you get disconnected errors when trying to checkout the SVN repo, you can finish the checkout with `while true; svn cleanup && svn up; sleep 2; done`.
- On Ubuntu you can install SDL dependencies with:
```
sudo apt-get install -y libsdl2-mixer-dev libsdl2-image-dev libsdl2-dev libsdl2-2.0
```
- Building should be easy: `cd src/ &&  make`.
