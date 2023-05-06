
##########    ##########    ##########    ##########    ##########
#        #    #        #    #        #    #        #    #        #
#        #    #        #    #        #    #        #    #        #
#     #  #    #     #  #    #     #  #    #     #  #    #     #  #
#        #    #        #    #        #    #        #    #        #
#        #    #        #    #        #    #        #    #        #
##########    ##########    ##########    ##########    ##########

### SO MANY DOORS, WHICH ONE TO CHOOSE??? ###

import random
FLAG = 'REDACTED'
REQ_WINS = 10
DOORS = 10
usr_choice = ''
random.seed(123049)
wins = 0
def play():
    comp_choice = random.randint(-10000, 10000)
    comp_choice %= DOORS
    print(comp_choice)
    print(f'\nYou are presented with {DOORS} doors, {DOORS - 1} are haunted and 1 will allow you to pass.')
    door_choice = int(input('Which will you choose?\n'))
    print(f'\nYou chose door {door_choice}...')
    return door_choice == comp_choice
print(f'Welcome to Ghost Game! Win {REQ_WINS} times in a row for your reward.')
while True:
    print('\n1. Play\n2. Quit')
    usr_choice = input()
    if usr_choice == '1':
        if play():
            print('You chose the right door and survived! Phew.')
            wins += 1
        else:
            print('That door had a ghost behind it. RIP.')
            wins = 0
    elif usr_choice == '2':
        break
    else:
        print('Invalid input.')
    if wins >= REQ_WINS:
        print('You must have insane luck! Here is your treasure:')
        print(FLAG)
