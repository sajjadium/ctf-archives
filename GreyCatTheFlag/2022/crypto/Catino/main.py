from secrets import randbits
from decimal import Decimal, getcontext

FLAG = <REDACTED>

ind = 100
randarr = []
maxRound = 5000
winTarget = 100000
winIncr = 1000

getcontext().prec = maxRound + 1000

def prep():
    global randarr
    print("\nGenerating random numbers....", flush=True)
    n = Decimal(randbits(2048))
    p = Decimal(1/4)
    k = str(n**p).split('.')[1]
    randarr = list(k)
    print("Generation complete!\n", flush=True)


def nextRand():
    global ind
    assert ind < len(randarr)
    res = int(randarr[ind])
    ind += 1
    return res


def menu():
    print('''
                    &                                                           
                    #&&&                                       &                
                    .&&&&&.          (((((.((((((((.       #&&&                 
                     &&&&&&&&      (((((((((((((((/((  ,&&&&&&&                 
                     &&&   &&&&/  (((   ((((((((((((((&&&/@&&&                  
                     &&&     ((((((((/              (((   &&&                   
                     &&&     ((((((((((((((((((((((((((((@&&&                   
                     &&&  @&&&&&/((((((((((((((((((((((((((&                    
                     &&&&&&&&&&&&&&&&&&@/((((((((((((((%&&&                     
                     &&&&&&&&&&&&&&&&&&&&&        &&&&&&&&&                     
                   &&&&&&&&&%     @&&&&&            &&&&&&&&                    
                  &&&&&&&&%         &&&              @&&&&&&&.                  
                 &&&&&&&&&    @&&    &&    &&& @     .&&&&&&&&                  
                 &&&&&&&&&&   &&&&  &&&    &&&&&.    &&&&&&&&&&                 
                 &&&&&&&&&&&@     &&&&&&&          *&&&&&&&&&&&                 
                 &&&&&&&&&&&&&&&&&&,,,,,,&&&&&#@&&&&&&&&&&&&&&                  
                  &&&&&&&&&&&&&&&&&&&  &&&&&&&&&&&&&&&&&&&&&&&                  
                   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                   
                    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                     
                      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                       
                         &&&&&&&&&&&&&&&&&&&&&&&&&&&&&.                         
                             %&&&&&&&&&&&&&&&&&&&&                              
                             &&&&&&&&&&&&&&&&&&&&&                              
                             &&&&&&&&&&&&&&&&&&&&&                              
                             &&&&&&&&&&&&&&&&&&&&&                              
                             &&&&&&&&&&&&&&&&&&&&&                              
                              &&&&&&&&&&&&&&&&&&&&&&&&&,s
    ''')
    print("Hey there, I am catino! Meowww ~uwu~")
    print("Play a game with me and win the flag!\n")

    print("Game rule:")
    print("1. You start with $0")
    print("2. On each round, Catino choose a single digit secret number (0-9)")
    print("3. You try to guess Catino secret's number")
    print(f"4. If the guessed number matches the secret, then you earn ${winIncr}")
    print("5. If the guessed number does not match the secret, then you lose all of your money!")
    print(f"6. You win when you have ${winTarget}!")
    print(f"7. The game ends forcefully when the number of round exceeds {maxRound}", flush=True)

if __name__ == "__main__":
    menu()
    prep()

    round = 0; wrong = 0; player = 0

    while (player < winTarget and round < maxRound):
        round += 1
        print(f"Round: {round}")
        userIn = int(input("Guess the number (0-9): "))
        num = nextRand()
        if (num == userIn):
            print(f"You got it right! it was {num}")
            player += winIncr
        else:
            print(f"You got it wrong... it was {num}")
            player = 0
        print(f"You have ${player} left")
    
    if (player >= winTarget):
        print("Congratulations you are now rich! \(★ω★)/")
        print(FLAG)
    else:
        print("Sokay.. Try again next time (っ´ω`)ﾉ(╥ω╥)")