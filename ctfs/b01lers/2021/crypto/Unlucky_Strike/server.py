from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import sys, base64, time
from proprietary_data import *



def pkcs7(msg):
   padlen = 16 - (len(msg) & 0xf)
   return msg + bytes([padlen]*padlen)

def unpkcs7(padded):
   while True:
      if (len(padded) & 0xf) != 0 or len(padded) == 0: break
      padlen = padded[-1]
      if padlen < 1 or padlen > 16: break
      if any([ padded[-(i + 1)] != padlen for i in range(padlen)]): break
      return padded[:(-padlen)]
   raise ValueError


class Server:
   def __init__(self):
      self.key = get_random_bytes(32)

   def getTicket(self):
      nums = [int.from_bytes(get_random_bytes(2), "big")   for i in range(Nballs - 1)]
      traw = ",".join([ str(v) for v in nums])
      traw = ("numbers:" + traw).encode("ascii")
      IV = get_random_bytes(16)
      cipher = AES.new(self.key, AES.MODE_CBC, IV)
      ticket = IV + cipher.encrypt( pkcs7(traw + b"," + JOKER) )
      return base64.b64encode(ticket).decode("ascii")

   def redeemTicket(self, ticket):
      try:
         tenc = base64.b64decode(ticket)
         cipher = AES.new(self.key, AES.MODE_CBC, tenc[:16])
         traw = cipher.decrypt(tenc[16:])
         traw = unpkcs7(traw)
         nums = [v for v in traw[traw.index(b"numbers")+8:].split(b",")] [:Nballs]
      except (ValueError, IndexError):
         print("that is an invalid ticket")
         return False
      if any([ str(v).encode("ascii") not in nums  for v in self.numbers]):
         print(f"sorry, that ticket did not win anything")
         return False
      else:
         print(f"**JACKPOT**  -> Here is your reward: {FLAG}")
         return True

   def main(self):
      print( "      --------------------------------------------\n"
             "      Welcome to the 2021 B01lers Crypto Town Fair\n"
             "      --------------------------------------------\n"
             "\n"
             "Due to popular demand, our Super Jackpot Lottery [TM] returns this year as well. We are\n"
             "so confident in our not-entirely-fair algorithm that we are publicly releasing its source\n"
             "code. Chances for winning have never been smaller! Prizes have never been bigger!!!\n"
             "")
      ticket = self.getTicket()
      print( "Here is your complimentary raffle ticket:\n"
            f"{ticket}")
      print( "")
      time.sleep(1)
      sys.stdout.write(f"Draw commencing... [drumroll]")
      sys.stdout.flush()
      self.numbers = [int.from_bytes(get_random_bytes(3), "big")   for i in range(Nballs)]
      time.sleep(4)
      print( "... and the winning numbers are:\n"
            f"{self.numbers}\n"
             "")

      while True:
         print("Redeem a ticket:")
         t = input()
         if self.redeemTicket(t): break




if __name__ == "__main__":

   server = Server()
   server.main()

