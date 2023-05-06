Hint for beginners:

    The attached file contains a Python script named beginners_crypto_2021.py and a text file named output.txt. These two files indicate that the latter text file was the result of running the former Python script.
    You can see that the Python script reads the file flag.txt, encrypts it, and outputs it. Since flag.txt is not included in the distribution file, you will have to guess from the output results to find and answer the contents of the original flag.txt. This will be the purpose of this question.
    You will need a cryptographic library called Pycryptodome to run the attached Python script. Please run pip install pycryptodome to install it beforehand.
    In the Python script, there is a line from secret import e that reads the secret parameter e from secret.py, which is used to encrypt the flag. secret.py is of course not included in the distribution, so you will have to guess it.
        To run the script locally, you will need to create a temporary secret.py or rewrite the source code to define the parameters directly.
    Once you get a numerical value that represents the flag, convert it to a string using the reverse procedure of reading flag.txt and answer it. If you have the correct flag format (TSGCTF{...}), you've won!

