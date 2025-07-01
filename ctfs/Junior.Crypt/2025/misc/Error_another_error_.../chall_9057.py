from random import randint, shuffle
from copy import copy


def hamming_encode_7_4(data_bits):
    """Кодирование 4 бит данных в 7-битный код Хэмминга (7,4)
    Args:    data_bits: str - строка из 4 бит (например, '1101')
    Returns: str: 7-битная закодированная строка
    """
    if len(data_bits) != 4 or not all(bit in '01' for bit in data_bits):
        raise ValueError("Нужно 4 бита (например, '1101')")
    
    d1, d2, d3, d4 = map(int, data_bits)
    
    # Вычисляем контрольные биты (p1, p2, p3)
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    
    # Собираем закодированное сообщение (позиции 1-7)
    encoded = [p1, p2, d1, p3, d2, d3, d4]
    
    return ''.join(map(str, encoded))


hcode = [[(bin(i)[2:]).zfill(4), 0, (bin(i)[2:]).zfill(4)] for i in range(0,15)] + [[(bin(i)[2:]).zfill(4), 0, (bin(i)[2:]).zfill(4)] for i in range(0,15)]
shuffle(hcode)

for ind in range(0, len(hcode)):
    r = randint(0,10)
    hcode[ind][1] = r if r <= 6 else 0
    code0 = hamming_encode_7_4(hcode[ind][0])
    if r <= 6:
        code0 = code0[:r] + ('1' if code0[r] == '0' else '0') + code0[r+1:]
    hcode[ind][0] = copy(code0)

FLAG = 'grodno{Redacted_FLAG}'
err_flag = False
ROUNDS = 3

print(f"\nВсего раундов / Rounds: {ROUNDS}\n")

for round_num in range(0, ROUNDS):
    print(f"=== Round {round_num + 1} ===\n")

    answer = input(f"{hcode[round_num][0]} позиция:данные >>")
    if answer == f"{hcode[round_num][1]}:{hcode[round_num][2]}":
        print(f"Правильно / Right")
    else:
        print(f"Ошибка. Правильный ответ / Error. Good answer: {hcode[round_num][1]}:{hcode[round_num][2]}")
        err_flag = True
        break

if not err_flag:
    print(f"\nFlag is: {FLAG}")