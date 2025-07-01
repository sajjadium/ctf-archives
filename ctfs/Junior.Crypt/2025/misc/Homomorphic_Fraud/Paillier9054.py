from Crypto.Util.number import getPrime, bytes_to_long
import random

# Генерация ключей Paillier
def generate_keypair(bits=512):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    g = n + 1  # Стандартный выбор для g в Paillier
    lambda_ = (p - 1) * (q - 1)
    mu = pow(lambda_, -1, n)
    return (n, g), (lambda_, mu)

# Шифрование
def encrypt(m, pub_key):
    n, g = pub_key
    r = random.randint(1, n - 1)
    c = (pow(g, m, n**2) * pow(r, n, n**2)) % n**2
    return c

# Дешифрование
def decrypt(c, priv_key, pub_key):
    n, g = pub_key
    lambda_, mu = priv_key
    x = pow(c, lambda_, n**2)
    l = (x - 1) // n
    m = (l * mu) % n
    return m

# Инициализация

FLAG = "grodno{Redacted_Flag}"

pub_key, priv_key = generate_keypair()
balance = random.randint(0, 999999)      # Начальный баланс
enc_balance = encrypt(balance, pub_key)
end_balance = encrypt(1000000, pub_key)

print(f"[*] Public Key (n, g) = {pub_key}")
print(f"[*] Encrypted Balance = {enc_balance}")

# Обработчик "транзакций"
def process_transaction(enc_amount):
    global enc_balance
    # Гомоморфное сложение: Enc(balance + amount)
    enc_balance = (enc_balance * enc_amount) % (pub_key[0] ** 2)
    return enc_balance

# Пример работы сервера (имитация API)
if __name__ == "__main__":
    print("\n[*] Server is running. Send your transactions as `Enc(amount)`.")
    
    while True:
        try:
            user_input = int(input(">> Enc(amount) = "))
            new_enc_balance = process_transaction(user_input)
            print(f"[+] New Encrypted Balance = {new_enc_balance}")
            if decrypt(new_enc_balance, priv_key, pub_key) == decrypt(end_balance, priv_key, pub_key):
                print (f"Flag is: {FLAG}")
                break
            elif new_enc_balance > end_balance:
                print (f"Слишком много / Too many")
                break
        except:
            print("[!] Invalid input. Use integers.")