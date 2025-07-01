# for Users

#! /usr/bin/python3 -u

from random import randint
from Crypto.Util.number import getPrime

# Конфигурация
FLAG = 'CTF{zkp_basic_secret_123}'
ROUNDS = 2

# Параметры протокола
p = getPrime(512)   # Простое число
g = 2               # Генератор группы Zp*
x = randint(1,p-2)  # Секрет (g^x mod p = y)
y = pow(g, x, p)    # y

n_leak = 464

def main():

        print(f"\n=== Zero-Knowledge Proof: Prove You Know x ===")
        print(f"Параметры / Parameters: \np={p}, \ng={g}, \ny={y}\n")
        print(f"Докажите, что знаете x, такой что g^x ≡ y mod p\n")
        print(f"Всего раундов / Rounds: {ROUNDS}\n")

        err_flag = False
        for round_num in range(1, ROUNDS+1):
            print(f"=== Round {round_num} ===\n")

            # 1. Проверяющий генерирует r, отправляет C = g^r mod p. 
            #    Однако, в результате утечки, к Доказывающему приходит еще и 464 младших бита r
            r = randint(1, p-1)  # Случайный nonce
            C = pow(g, r, p)
            leak = r % 2**n_leak    # Утечка 

            print(f"C = g^r mod p: {C}")
            print(f"Утечка / leak(r): {leak}") # 464 младших бита r

            # 2. Проверяющий генерирует и отправляет  challenge e
            e = randint(1, 2**32)
            print(f"e = {e}")


            # 3. Доказывающий восстанавливает r и присылает s = (r + e*x) mod (p-1)
            print(f"Вычислите / Calculate s = (r + e*x) mod (p-1):")
            s = int(input().strip())

            # 4. Верификация
            left = pow(g, s, p)
            right = (C * pow(y, e, p)) % p
            if left != right:
                print(f"\nОшибка верификации / Verification failed!")
                print (f"Правильный s / Correct s is: {(r + e * x) % (p-1)}")
                print (f"Рaунд не пройден / Round not passed\n")
            else:
                print("Рaунд пройден / Round passed\n\n")
                err_flag = True
        
        # Все раунды пройдены
        if err_flag:
            print(f"Success! Flag: {FLAG}")
        else:
            print ("Не беда. Решите следующий раз ... / No problem. Decide next time ...")


if __name__ == "__main__":
    
    main()