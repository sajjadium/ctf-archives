import hashlib, random, time

flag = open('flag.txt', 'rb').read().strip()

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def roll(seed, round):
    return int(sha(f"{seed}-{round}"), 16) % 100

def main():
    seed = random.Random(int(time.time())).randbytes(16).hex()
    print(f"commitment:{sha(seed)}")
    print("Guess 5 rolls in a row (each between 0 and 99) to win!")

    streak = 0
    for round in range(10**9):
        try:
            guess = int(input(f"round {round}, streak {streak}/5, enter your guess: "))
        except (ValueError, EOFError):
            print("bye")
            return
        
        r = roll(seed, round)
        if guess == r:
            streak += 1
            print(f"roll was {r}, streak = {streak}")
            if streak >= 5:
                print(f"Congratulations! Here's your flag {flag}")
                return
        else:
            streak = 0
            print(f"roll was {r}, streak reset")
        

if __name__ == "__main__":
    main()