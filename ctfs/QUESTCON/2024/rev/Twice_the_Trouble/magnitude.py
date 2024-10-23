import math
import random

def xor_encrypt_decrypt(input_str, key):
    return ''.join(chr(ord(c) ^ key) for c in input_str)

def get_flag():
    # XOR-encoded flag
    encoded_flag = [92, 88, 72, 94, 89, 78, 66, 67, 118, 105, 61, 120, 111, 97, 62, 82, 121, 127, 61, 120, 111, 97, 62, 112]
    key = 13  # XOR key used for encoding
    flag = ''.join(chr(c ^ key) for c in encoded_flag)
    return flag

# Function to compare the magnitude of two numbers
def compare_numbers(num1, num2):
    if math.sqrt(num1**2) == 2 * abs(num2):
        print("The magnitude of the first number is exactly twice the magnitude of the second!")
        return True
    else:
        print("One of the numbers has a larger magnitude.")
        return False

def main():
    junk = [random.randint(1, 100) for _ in range(10)]
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        # Compare numbers and reveal flag if the condition is met
        if compare_numbers(num1, num2):
            print(f"Congratulations! Here's the flag: {get_flag()}")
        else:
            print("Try again with different numbers.")
    
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    main()
