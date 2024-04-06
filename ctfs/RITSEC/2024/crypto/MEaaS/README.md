Sophie, one of Anthony's bosses, encrypts a lot of her data using RSA. We managed to recover the modulus and ciphertexts of her last three encryptions as well as an API key for a MEaaS (modular exponentiation as a service) application she uses for her RSA calculations. You can connect to the service via netcat as shown below. We've discovered that the service stores the last 16-bit exponent and modulus she used, and we know she used the same ones for all three encryptions. Additionally, the service adds an extra layer of security by encrypting the result using AES with a secret key. Lastly, something interesting about the MEaaS is that you can provide a "slice" of the bits of the exponent to use. For example, consider the exponent 14 which is 1110 in binary. If you provide a slice of 1, the exponent used will be the single least significant bit (0 in both binary and decimal). Similarly, a slice of 3 would make the exponent 110 (in binary, or 6 in decimal). Given this information and access to the MEaaS, can you determine what she encrypted?
n = 1970384981
c1 = 184323288
c2 = 306942680
c3 = 1791553791
API Key: abadbd796f1b2ae8bd82e1195ad12373
