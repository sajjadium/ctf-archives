import random
NUMS = list(range(10**4))
random.shuffle(NUMS)
tries = 15
while True:
    try:
        n = int(input('Enter (1) to steal and (2) to guess: '))
        if n == 1:
            if tries==0:
                print('You ran out of tries. Bye!')
                break
            l = map(int,input('Enter numbers to steal: ').split(' '))
            output = []
            for i in l:
                assert 0<= i < len(NUMS)
                output.append(NUMS[i])
            random.shuffle(output)
            print('Stolen:',output)
            tries-=1
        elif n == 2:
            l = list(map(int,input('What is the list: ').split(' ')))
            if l == NUMS:
                print(open('flag.txt','r').read())
                break
            else:
                print('NOPE')
                break
        else:
            print('Not a choice.')
    except:
        print('Error. Nice Try...')

