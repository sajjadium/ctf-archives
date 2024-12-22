import hashlib
from typing import List

class CustomMAC:
    def __init__(self):
        self._internal_state = b""
        
    def update(self, message: bytes) -> None:
        if not self._internal_state:
            self._internal_state = self.get_key() + message
        else:
            self._internal_state += message
            
    def get_key(self) -> bytes:
        return open("key.txt", "rb").read().strip()
            
    def digest(self) -> bytes:
        return hashlib.sha256(self._internal_state).digest()[:8]

class TokenManager:
    def __init__(self):
        self._mac = CustomMAC()
        self._seen_tokens: List[bytes] = []
        
    def verify_and_store(self, message: bytes, token: bytes) -> bool:
        self._mac = CustomMAC()
        self._mac.update(message)
        expected_token = self._mac.digest()
        
        if token != expected_token:
            print(f"Invalid token! Expected token: {expected_token.hex()}")
            return False
            
        if token in self._seen_tokens:
            print("Token already used!")
            return False
            
        self._seen_tokens.append(token)
        return True

def main():
    print("Welcome to the Token Verification Challenge!")
    print("============================================")
    print("Rules:")
    print("1. Submit message-token pairs")
    print("2. Each token must be valid for its message")
    print("3. You cannot reuse tokens")
    print("4. Get 64 valid tokens accepted to win!")
    print("\nFormat: <hex-encoded-message> <hex-encoded-token>")
    print("Example: 48656c6c6f 1234567890abcdef")
    
    manager = TokenManager()
    successes = 0
    
    for i in range(128):
        try:
            print(f"\nAttempt {i+1}/128")
            print("Enter your message and token: ", end='')
            user_input = input().strip().split()
            
            if len(user_input) != 2:
                print("Invalid input format!")
                continue
                
            message = bytes.fromhex(user_input[0])
            token = bytes.fromhex(user_input[1])
            
            if manager.verify_and_store(message, token):
                successes += 1
                print(f"Success! {successes}/64 valid tokens verified")
                
                if successes >= 64:
                    print("\nCongratulations! You beat the challenge!")
                    with open("flag.txt", "r") as f:
                        print(f.read().strip())
                    break
            
        except Exception as e:
            print(f"Error: {str(e)}")
            continue
            
    if successes < 64:
        print("\nChallenge failed! Not enough valid tokens.")

if __name__ == "__main__":
    main()