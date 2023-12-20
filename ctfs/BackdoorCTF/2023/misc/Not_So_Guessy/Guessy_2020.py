Secret_Number = "REDACTED"
Flag = "REDACTED"

AI = {2:'Scissors', 1:'Paper', 0:'Rock'}
win = {'Rock':'Paper','Paper':'Scissors','Scissors':'Rock'}
draws = 0
wins = 0

print("Welcome to The Guessy Game.")
print("To get The Flag, you have to beat the AI I made in Rock, Paper, Scissors until it can't take the losses and self-destructs.")
print("However if you lose once, You Lose.")
print("Beware! If the AI draws you twice, it will analyse your mind and you will never be able to defeat it ever.")

while Secret_Number:
    hand = AI[Secret_Number % 3]
    Secret_Number//=3
    print()
    print(f"Wins : {wins}, Draws : {draws}")
    print('Rock, Paper, Scissors!')
    guess = input()
    if guess == hand:
        print("Ah, Seems like its a draw.")
        draws += 1
        if draws == 2:
            print("The AI now knows your every move. You will never win.")
            exit()
    elif guess == win[hand]:
        wins += 1
        if Secret_Number==0 :
            print("Fine. You got me. It wasn't an AI it was just a simple Python Code.")
            print('Here is your Flag. Take it!')
            print()
            print(Flag)
            print()
            exit()
        print('Okay you guessed right this time. But its not enough to defeat my AI.')
    else : 
        print("Haha. I knew you didn't have it in you.")
        print("You guessed wrong. Bye byee")
        exit()