from django.contrib.auth.hashers import PBKDF2PasswordHasher

class PBKDF2LowIterationHasher(PBKDF2PasswordHasher):
    """
        Custom password hasher to make password cracking doable in a reasonable time period
    """
    iterations = 1000