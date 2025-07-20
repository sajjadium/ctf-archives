Author: Frank01001

GameBoxArt

    Hey, my cousin lent me this Wii game we used to play together when we were kids. It was really cool because the developers also sold custom SD cards with additional cards to be added to the game. Man those were the days. Anyway I heard on Reddit that you can use it to install the Homebrew Channel. Anyone know how to do that?

Goal: get the contents of /sys/flag in system NAND Remote: Dolphin 2506a emulator on Linux. The build has been patched to enable the use of networking in TAS (so you can provide us input). The patch is included in the attachments.

You will be able to upload your SD card files and and a TAS recording. You will not be given access to the screen and no screenshots will be made.

You are advised to use the same build on the same OS to avoid problems. The web server used by the game in localhost is provided as a "dummy" server that the game could have used in its intended functionality, but has not bearing on the challenge.

The run.sh is provided, as it is the same configuration used in the server. This will use Dolphin in "headless" mode, so you will not see the emulator window. Use the script at the very end to check whether your exploit works in this environment.

Troubleshooting:

    If you encounter a bus error, it is likely the small shared memory limit in Docker. You can try to increase it by adding --shm-size=2g to the docker run command.
    Dolphin networking may encounter some issues on Windows

Please request an instance opening a ticket when you solve it locally. Please attach a proof you solved the challenge locally.
