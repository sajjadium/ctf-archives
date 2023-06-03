import bcrypt
import jwt
import secrets


class userUtils:

    def __init__(self) -> None:
        pass

    def hash_verifier(self, password, recoveredPassword):
        result = False
        exception = False

        try:
            result = bcrypt.checkpw(password.encode(), recoveredPassword.encode())
        except Exception:
            exception = True

        return result \
            if recoveredPassword.startswith("$2y$") and not exception else False

    def jwtSignerMethod(self, dictToEncode, jwt_token):
        return jwt.encode(dictToEncode, jwt_token, algorithm="HS256")

    def generateRandomToken(self, length):
        return secrets.token_hex(length)
