I heard proof of stake was the new cool thing, so i converted my PoW blockchain over to PoS.

Can you double check that the system works ok?

    Due to an unintended bug, we had to upload a new handout. Below is the diff with the old handout.

diff --git a/chal.py b/chal.py
--- a/chal.py
+++ b/chal.py
@@ -157,6 +157,8 @@ if __name__ == "__main__":
                 if not check_ticket(winner_name, i):
                     print("why did you submit an invalid ticket?")
                     exit()
+                else:
+                    break
             elif command == "win":
                 name, sig = input("win claim (name sig):").split()
                 verify_win((name, int(sig)))
