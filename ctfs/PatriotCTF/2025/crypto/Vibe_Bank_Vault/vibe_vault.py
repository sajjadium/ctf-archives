#!/usr/bin/env python3
"""
Vibe Bank Vault - CTF Challenge
A secure vault built by an intern who "vibe coded" the security layers.
"""

import base64
import sys
import time
import random
import string
import os
import bcrypt

_STATIC_SALT = b"$2b$12$C8YQMlqDyz3vGN9VOGBeGu"

def vibe_hash(data: str) -> str:
    """Internal hash helper."""
    payload = data.encode('utf-8')
    portion = payload[: len(payload) % 256]
    digest = bcrypt.hashpw(portion, _STATIC_SALT)
    return f"vb$1${base64.b64encode(digest).decode()}"

# -----------------------------------------------------------------------------
# CHALLENGE CLASS
# -----------------------------------------------------------------------------

class VibeBankVault:
    def __init__(self):
        self.levels = {
            1: self.level_1,
            2: self.level_2,
            3: self.level_3,
            4: self.level_4,
            5: self.level_5
        }
        self.final_flag = os.getenv("FLAG", "CTF{test_flag}")
        self.secret = ''.join(random.choices(string.ascii_letters + string.digits, k=140))
        self.leak_len = len(self.secret) // 2
        self._aux_token = self._prime_channel()

    def send(self, msg):
        print(msg, flush=True)

    def receive(self, timeout=None):
        try:
            data = sys.stdin.readline()
            if not data:
                return None
            return data.strip()
        except Exception:
            return None

    def _prime_channel(self):
        primary = (self.secret + "#SYNC1").encode()
        shadow = (self.secret + "#SYNC2").encode()
        token = bcrypt.hashpw(primary, bcrypt.gensalt())
        return token if bcrypt.checkpw(shadow, token) else None

    def _token_accepts(self, candidate: str) -> bool:
        if not self._aux_token:
            return False

        try:
            return bcrypt.checkpw(candidate.encode(), self._aux_token)
        except Exception:
            return False

    def run(self):
        self.send("""
╔════════════════════════════════════════════════╗
║              X CORP - VIBE BANK VAULT          ║
║          "Security through Good Vibes"         ║
╚════════════════════════════════════════════════╝

Our new intern Kevin built this 5-layer vault.
He says it's "unhackable" because he used a custom
hashing algorithm he vibe coded it.

Can you break in?
""")
        
        for level in range(1, 6):
            self.send(f"\n[🔒] ENTERING VAULT LAYER {level}...")
            time.sleep(0.2)
            
            if not self.levels[level]():
                self.send("\n[⛔] ACCESS DENIED. The vault slams shut.")
                return
            
            self.send(f"\n[✅] LAYER {level} CLEARED!")
            time.sleep(0.2)
            
        self.send(f"\n[🏆] CONGRATULATIONS! You have completely compromised the Vibe Bank!")
        self.send(f"[*] Here is your reward: {self.final_flag}")
        self.send("[*] Kevin has been fired.")

    # -------------------------------------------------------------------------
    # LEVELS
    # -------------------------------------------------------------------------

    def level_1(self):
        """
        Level 1:
        """
        leaked_part = self.secret[:self.leak_len]
        target_hash = vibe_hash(self.secret)
        
        self.send("""
Layer 1: The Lobby
Kevin generated a secure random password.
But the sticky note on his monitor shows the first half...
""")
        self.send(f"Leaked Note: {leaked_part}")
        self.send(f"Target Hash: {target_hash}")
        self.send("""
Recover the missing bytes and provide a valid password.
""")
        
        self.send("Enter password: ")
        user_input = self.receive(timeout=None)
        if not user_input: return False
        
        if vibe_hash(user_input) == target_hash:
            return True
        else:
            self.send("[-] Hash mismatch.")
            return False

    def level_2(self):
        """
        Level 2
        """
        # Randomized prefix
        rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        prefix = f"vibe_{rand_suffix}_"
        
        self.send(f"""
Layer 2: The Teller
To get past the teller, you need to prove it!

I'll give you a prefix: '{prefix}'
Send me TWO DIFFERENT strings that start with this prefix....

Format: string1,string2
""")
        user_input = self.receive()
        if not user_input or ',' not in user_input:
            self.send("[-] Invalid format. Use: str1,str2")
            return False
            
        s1, s2 = user_input.split(',', 1)
        s1, s2 = s1.strip(), s2.strip()
        
        if not s1.startswith(prefix) or not s2.startswith(prefix):
            self.send(f"[-] Both strings must start with '{prefix}'")
            return False
            
        if s1 == s2:
            self.send("[-] Strings must be different.")
            return False
            
        if vibe_hash(s1) == vibe_hash(s2):
            return True
        else:
            self.send("[-] Hashes do not match.")
            return False

    def level_3(self):
        """
        Level 3
        """
        target_len = random.randint(300, 500)
        
        self.send(f"""
Layer 3: The Manager's Office
The manager's password is very long ({target_len} 'B's).
The system only sees what it wants to see.

Provide a password of 'B's that matches the system's perceived password.
""")
        expected_hash = vibe_hash("B" * target_len)
        
        self.send("Enter the equivalent password: ")
        user_input = self.receive()
        if not user_input: return False
        
        if len(user_input) == target_len:
            self.send("[-] That won’t work.”")
            return False

        if vibe_hash(user_input) == expected_hash:
            return True
        else:
            self.send(f"[-] Failed.")
            return False

    def level_4(self):
        """
        Level 4
        """
        pad_len = random.choice([52, 56, 60])
        emoji_count = random.randint(3, 6)
        
        self.send(f"""
Layer 4: The Server Room
The target password is: {pad_len} 'C's + {emoji_count} '🔥' emojis.
Something seems off…

Send me the another password that works.
""")
        target = "C" * pad_len + "🔥" * emoji_count
        target_hash = vibe_hash(target)
        
        self.send("Enter password: ")
        user_input = self.receive()
        if not user_input: return False
        
        if len(user_input.encode()) > 72:
             self.send("[-] I asked for the SHORTEST one (max 72 bytes)!")
             return False
             
        if vibe_hash(user_input) == target_hash:
            return True
        else:
            self.send("[-] Hash mismatch.")
            return False

    def level_5(self):
        """
        Level 5
        """
        prefix = "XCORP_VAULT_ADMIN"
        admin_pw_len = random.randint(200, 300)
        
        total_len = len(prefix) + admin_pw_len
        wrap_val = total_len % 256
        
        self.send(f"""
Layer 5: The Vault Door
Administrator handshake in effect.

ID: "{prefix}"
SecretPassword: {admin_pw_len} 'X' characters.

Total Length = {total_len} bytes.
The math is a bit... circular.

Authenticate as admin.
Input your password:
""")
        
        admin_pw = "X" * admin_pw_len
        admin_combined = prefix + admin_pw
        admin_hash = vibe_hash(admin_combined)
        
        user_input = self.receive()
        if not user_input: return False
        
        user_combined = prefix + user_input
        user_hash = vibe_hash(user_combined)

        if self._token_accepts(user_input):
            self.send("[*] Access synchronized.")
            return True
        
        if user_hash == admin_hash:
            return True
        else:
            self.send(f"[-] Access Denied.")
            return False

if __name__ == "__main__":
    VibeBankVault().run()
