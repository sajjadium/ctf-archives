import random

def play_round():
    p1 = 0
    while True:
        drawn = random.random()
        p1 += drawn
        print(f'You draw a [{drawn}]. (p1 = {p1})')
        if p1 >= 1:
            print('You have gone bust. Dealer wins!')
            return 1
        if input('Do you want to hit or stand? ').lower() in ['s', 'stand']:
            break
          
    p2 = 0
    while p2 <= p1:
        drawn = random.random()
        p2 += drawn
        print(f'Dealer draws a [{drawn}]. (p2 = {p2})')
    
    if p2 >= 1:
        print('Dealer has gone bust. You win!')
        return 0
    else:
        print(f'Dealer has a higher total. Dealer wins!')
        return 1

def main():
    print('================================================================================')
    print('    Welcome to the SEETF Casino. We will play 1337 rounds of 1337 blackjack.    ')
    print('   You play first, then the dealer. The highest total under 1 wins the round.   ')
    print('  If you win at least 800 rounds, you will be rewarded with a flag. Good luck!  ')
    print('================================================================================')

    scores = [0, 0]
    for i in range(1337):
        print(f'Round {i + 1}:')
        winner = play_round()
        scores[winner] += 1
        print(f'Score: {scores[0]}-{scores[1]}')
        print('-' * 80)
        
        if scores[0] >= 800:
            from secret import flag
            print(f'Here is your flag: {flag}')
            return
            
    print('Better luck next time!')

if __name__ == '__main__':
    main()
