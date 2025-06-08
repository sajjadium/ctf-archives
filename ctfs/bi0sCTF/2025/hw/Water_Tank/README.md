Hardware

You've gained access to a water tank control system at a critical infrastructure facility. The tank is currently filling with water and will soon overflow! Your mission is to understand the industrial control protocol to find and close the right valves before it's too late.

A packet capture of the network traffic is provided. Analyze it to extract the login credentials that provide the access to the system.

+-------------------- System Information --------------------+
 Holding Registers : 200                                    
 Coils             : 100                                    
 Discrete Inputs   : 100                                    
 Input Registers   : 100                                    
 Tank Status       : 0=normal, 1=high, 2=critical           
 Inverted          : 0=CLOSED, 1=OPEN                       
 Normal            : 1=CLOSED, 0=OPEN                       
+------------------------------------------------------------+

- No. of open valves = HR 10
- Flow Rate = HR 11
- Tank Level = HR 12

You need to manually update the flag obtained from the server.

Example Flag: bi0s{admin_password_f4k3_fl4g}

Author: 3ji
Flag Format:
bi0s{username_password_obtained_flag}
