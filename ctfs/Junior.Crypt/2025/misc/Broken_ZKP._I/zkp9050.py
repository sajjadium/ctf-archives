#! /usr/bin/python3 -u

from random import randint
from Crypto.Util.number import getPrime


# Конфигурация
FLAG = 'CTF{zkp_basic_secret_123}'
ROUNDS = 5

# Параметры протокола
p = getPrime(512)   # Простое число
g = 2               # Генератор
x = randint(1,p-2)  # Секрет (g^x mod p = y)
y = pow(g, x, p)    # y

r = randint(1,p-1)
C = pow(g, r, p)

def verify(s, e):
    return pow(g, s, p) == (C * pow(y, e, p)) % p

def main():
        c_mist = 0

        print(f"\n=== Zero-Knowledge Proof: Prove You Know x ===")
        print(f"Параметры / Parameters: p={p}, g={g}, y={y}, r={r}\n")
        print(f"Всего раундов / Rounds: {ROUNDS}\n")

        for round_num in range(1, ROUNDS+1):
            print(f"=== Round {round_num} ===\n")

            # 1. Проверяющий отправляет challenge e
            e = randint(1, pow(2,32))
            print(f"Challenge e = {e}")
            
            # 2. Доказывающий отправляет s = (r + e*x) mod (p-1)
            print("Отправьте / Send s = (r + e*x) mod (p-1): ")
            
            s = int(input().strip())

            # 3. Верификация
            #left = pow(g, s, p)
            #right = (C * pow(y, e, p)) % p
            if verify(s, e): #left != right:
                c_mist += 1
                print(f"\nОшибка верификации / Verification failed!\n")
                print (f"s = {(r + e*x) % (p-1)}")
                if c_mist > 2:
                    return
            
            print("Рaунд пройден / Round passed!\n\n")
        
        # Все раунды пройдены
        print ("Все раунды пройдены. Может все-таки знаете, чему равен x:")
        x_proof = int(input().strip())
        if x == x_proof:
            print(f"Success! Flag: {FLAG}")
        else:
            print ("Вы ошились / You are mistake ...")

if __name__ == "__main__":
    
    main()