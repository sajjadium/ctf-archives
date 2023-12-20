Secret_Number = "REDACTED"
Flag = "REDACTED"

coin = {1:'Heads', 0:'Tails'}
wins = 0

print("Welcome to The Guessy Game.")
print("To get The Flag, you have to beat me in Heads and Tails until I admit defeat.")
print("However if you lose once, You Lose.")

while Secret_Number:
    draw = coin[Secret_Number % 2]
    Secret_Number//=2
    print()
    print(f"Wins : {wins}")
    print('Heads or Tails?')
    guess = input()
    if guess == draw:
        wins += 1
        if Secret_Number==0 :
            print('Fine. I give up. You have beaten me.')
            print('Here is your Flag. Take it!')
            print()
            print(Flag)
            print()
            exit()
        print('Okay you guessed right this time. But its not enough to defeat me.')
    else : 
        print("Haha. I knew you didn't have it in you.")
        print("You guessed wrong. Bye byee")
        exit()