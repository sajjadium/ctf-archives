We have infiltrated the shadowy organization and set up a tunnel to their secret mainframe (nc chal.b01lers.com 25002). Unfortunately, any server output is encrypted via plain RSA. All is not lost, however, because a trusted insider can provide temporary access to their test server (nc chal.b01lers.com 25001). The test server has an additional feature that allows for toggling encryption on and off through a modified output function
   def output(self, msg):
       if self.debug: print(msg)
       else:          normal_encrypted_output(msg)
Your mission, should you accept it, is to leverage the given access and extract the secret data from the mainframe within the next 48 hours. Time is critical, so manage resources wisely. This message will self-destruct in 5.. 4.. 3.. 2.. 1..
