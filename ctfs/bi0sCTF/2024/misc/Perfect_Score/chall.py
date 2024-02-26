import random
import os
from math import gcd
flag = open("flag.txt").read().strip()
menu = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   50 shots, hit the spot!                                                    ║
║ ____________________________________________________________________________ ║
║                                                                              ║
║   1. Verify divisibility                                                     ║
║   2. Verify co-prime array                                                   ║
║   3. Submit your guess                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def handle_client():
    cnt = 0
    for _ in range(10):
        print(menu)
        x = random.randint(1, 10000)
        for _ in range(50):
            print("╔══════════════════════════════════════════════════════════════════════════════╗")
            print("║ [+] Choose an option (1, 2, or 3):                                           ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
            print(">> ",end="")
            option = input().strip()

            if option == '1':
                print("__________________________________________________")
                print("▏[CHOICE 1] Enter a number to check divisibility: ▏")
                print("▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
                print("[+] Your number : ",end="")
                y = int(input().strip())
                response = "Yes" if x % y == 0 else "No"
                print(f"[+] Is x divisible by {y}? {response}")
                print("")

            elif option == '2':
                print("__________________________________________________")
                print("▏[CHOICE 2] Enter an array (e.g. 2,3,5):          ▏")
                print("▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
                print("Your Array : ",end="")
                array_str = input().strip()
                array = [int(num) for num in array_str.split(",")]
                response = "Yes" if any(gcd(x, y) > 1 for y in array) else "No"
                print(f"Is there a y in [{array_str}] such that gcd(x, y) > 1? {response}")
                print("")

            elif option == '3':
                print("__________________________________________________")
                print("▏[CHOICE 3] Submit your guess for x:              ▏")
                print("▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
                print("Your guess : ",end="")
                guess = int(input().strip())
                if guess == x:
                    print("Congratulations! Your guess is correct.")
                    print("")
                    cnt += 1
                    break
                else:
                    print("[+] Incorrect guess. Try again.")
                    exit(0)

            else:
                print("❯❯ Invalid option. Please select 1, 2, or 3.")
                exit(0)
        
    if cnt == 10:
        print(f"Congratulations! You have guessed all 10 numbers correctly. Here is your flag: {flag}")


if __name__ == "__main__":
    try:
        handle_client()
    except:
        exit(0)