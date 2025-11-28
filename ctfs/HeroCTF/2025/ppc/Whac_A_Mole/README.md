very-easy
The Whac-A-Mole game is fairly simple. But knowing how many moles there is a clear plus. Can you count them for me?

TCP: 

Note to begginers #1:Croping a mole model out, and using an exact pixel comparison is often not the best way to approach this problem. This is mainly due to different softwares blending pixels together when pasting an image on an other. In the current case, the background image and the moles have pretty different main colors. You could use this to create a mask. The opencv function connectedComponentsWithStats can count elements, when provided with a mask.

Note to begginers #2: An AI model would find a working solution very easily. I would however advise to try and work out a solution yourself if speed is not of the essence for you.

Note to begginers #3: Please find attached a template that will help you handle the interactions with the challenge.

Format: ^Hero{\S+}$
Author: Log_s
