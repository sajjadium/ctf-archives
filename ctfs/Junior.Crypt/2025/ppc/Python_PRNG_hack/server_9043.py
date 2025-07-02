import time
import random
import math

flag = "FAKE_FLAG"

m=math.ceil(time.time()*1000000)
a = 2**10
b = 2**30

random.seed(m)
rand_numbers = []

d = """
Попробуем взломать генератор псевдослучайных чисел (ПСЧ) Python.
Считаем, что ПСЧ создаются функцией randint стандартной библиотеки random. 
Вы можете попросить несколько последовательных ПСЧ, до 1000 штук.
А затем вы должны угадать следующее ПСЧ."""
print (f"{d}\n\n")

print ('1. Получить следующее число')
print ('2. Угадать следующее число')
ind = 0

while True:
    if ind == 1000:
        print ('Слишком долго думаешь. Отдохни ...')
        break
    inp = input('> ')
    if inp == '1':
        print (f"Следующее число: {random.getrandbits(32)}")
    elif inp == '2':
        ans = int(input('Ваше число: '))
        my_ans = random.getrandbits(32)
        if ans == my_ans:
            print (f"\nФлаг: {flag}")
        else:
            print (f"\nОшибка. Мое число: {my_ans}")
        break
    ind += 1