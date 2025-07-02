import math
import time

flag = "FAKE_FLAG"

m=math.ceil(time.time()*1000000)
a=2**15-1
b=2**51-1

x = m
rand_numbers = [x,]

for i in range(1,50):
    x = (a*x + b) % m
    rand_numbers.append(x)
    
d = """
Попробуем взломать Линейный Конгруэнтный Генератор псевдослучайных чисел (ПСЧ).
Его формула: Xn+1 = (A * Xn + B) mod M
Вы можете попросить несколько последовательных ПСЧ, до 50 штук.
А затем угадать следующее ПСЧ."""
print (f"{d}\n\n")
print ('1. Получить следующее число')
print ('2. Угадать следующее число')
ind = 0

while True:
    if ind == len(rand_numbers):
        print ('Слишком долго думаешь. Отдохни ...')
        break
    inp = input('> ')
    if inp == '1':
        print (f"Следующее число: {rand_numbers[ind]}")
    elif inp == '2':
        ans = int(input('Ваше число: '))
        if ans == rand_numbers[ind]:
            print (f"\nФлаг: {flag}")
        else:
            print (f"\nОшибка. Мое число: {rand_numbers[ind]}")
        break
    ind += 1