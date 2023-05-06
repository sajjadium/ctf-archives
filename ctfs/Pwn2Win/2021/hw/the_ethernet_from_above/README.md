Most of the obscure activities conducted by the Rhiza government are carried out on the continent to stay out of the Island's commoners' eyes and prevent information leakage. However, buildings on the Island storing potentially compromising material, such as the human genetics centre, have a rigid access control system.

Laura managed to compromise some computers in the government lab that develops this system. When analyzing the project, she found that the weakest point seems to be the electronic board that checks whether the access code to enter the buildings is correct. There is nothing special about the board itself: it is a Colorlight 5A-75B V7.0 board that, apparently, could be found very easily before the war. What is interesting is the bitfile programmed to the board, which is developed by the government lab.

Laura got access to the bitfile that the lab is testing. The specifications accompanying the bitfile state that the board can be accessed at 200.18.104.100 on UDP port 6000 after being connected to the network. Upon receiving the correct access code, it returns a datagram beginning with OK. Otherwise, it returns NOK. The project is apparently based on a customized version of LiteEth. Still, Laura was unable to gain access to the complete source code.

Reverse engineer the bitfile to find out which access code is accepted by the board.

Curiosity: If you don't have a Colorlight and want to see the bitfile working, you can submit it to Rhiza's test infrastructure. But it probably won't help you to solve the challenge. You really need to reverse engineer the bitfile.
