import random

def shift_text_file(input_file, output_file):
    # Read content from the input file
    with open(input_file, 'r') as file:
        text_content = file.read()
    # Generate a random number from 0 to 50 for shifting
        num = random.randint(0, 50)
        print(num)
    # Shift the content by adding spaces
        new_text_content = ''.join([chr(ord(i) ^ num) for i in text_content])

    # Write the encrypted to the output file
    with open(output_file, 'w') as file:
        file.write(new_text_content)



input_text_file = 'flag.txt'
output_shifted_text_file = 'encrypted.txt'
shift_text_file(input_text_file, output_shifted_text_file)