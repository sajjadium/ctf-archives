from random import randint

FLAG = 'REDACTED_FLAG'
ROUNDS = 3

# Параметры протокола
p = 23               # Простое число
g = 5                # Генератор
x = randint(1,p-2)   # Секрет (g^x mod p = y)
y = pow(g, x, p)     # y



def main():
        print(f"\n=== Zero-Knowledge Proof: Prove You Know x ===")
        print(f"Параметры / Parameters: {p=}, {g=}, {y=}")
        print(f"Всего раундов / Rounds: {ROUNDS}\n")

        for round_num in range(1, ROUNDS+1):
            print(f"=== Round {round_num} ===\n")

            # 1. Доказывающий выбирает r и отправляет C = g^r mod p
            print("Выберите r и отправьте C = g^r mod p / Select r and send C = g^r mod p: ")
            C = int(input().strip())

            # 2. Проверяющий отправляет challenge e
            e = randint(1, 100)
            print(f"Challenge e = {e}")
            
            # 3. Доказывающий отправляет s = r + e*x mod (p-1)
            print("Отправьте / Send s = r + e*x mod (p-1): ")

            s = int(input().strip())

            # 4. Верификация
            left = pow(g, s, p)
            right = (C * pow(y, e, p)) % p
            if left != right:
                print(f"\nОшибка верификации / Verification failed!\n")
                return
            
            print("Рaунд пройден / Round passed!\n\n")
        
        # Все раунды пройдены
        print(f"Success! Flag: {FLAG}")

if __name__ == "__main__":

    main()
