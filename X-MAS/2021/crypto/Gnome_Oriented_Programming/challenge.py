import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OTPGenerator(metaclass=Singleton):
    _OTP_LEN = 128

    def __init__(self):
        self.otp = os.urandom(OTPGenerator._OTP_LEN)

    def get_otp(self):
        return self.otp
