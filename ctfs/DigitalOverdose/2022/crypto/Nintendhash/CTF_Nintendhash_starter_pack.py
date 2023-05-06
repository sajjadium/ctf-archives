import hashlib
import ninhash

"""
To use the Nintendhash hashing function, just call
ninhash.Nintendhash(bytestring), with bytestring being a... byte string.
Here's an example if needed :

print("This is an example of message and digest with Nintendhash : ")
message = b"Are you sure this hash function is secure ?"
print("message is : ",message)
digest = ninhash.Nintendhash(message)
print("digest with Nintendhash is : ", digest)

"""


"""
Here's your message. Your goal is to add a 64 bit nonce at the end of the
message, with initial value 0, and increment it until you find the smallest
nonce that creates a collision with the initial message (i.e. you will
find a second pre-image).

The minimal nonce value is the flag you're searching for (we're searching
for the integer value of this nonce).

"""

message = b"To catch them is my real test. To train them is my cause."
digest = ninhash.Nintendhash(sec_image_message)
nonce = 0

# TODO : Find the minimal nonce for a second pre-image. That nonce is your flag.
