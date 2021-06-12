
# weebox.py

Usage:

```py
% python weebox.py bonjour
signature: 6d6c3064db439812dedbe1ad676d5a404cf19a7b40327396baf70f072e95797a37e394e59e8f323a5dd2e1fd1c58b181015c9ae01c822e1b08f811b0c90b59bb
public key: 9274d0bb1bd842d732a3ddc415032e45efa0130d8140a4fa77e67e284224968e
```

Once extracted, the flag is the private key deciphered with the AES null key:
```
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

cipher = Cipher(algorithms.AES(bytes(32)), modes.ECB())
decryptor = cipher.decryptor()
print(decryptor.update(private_key) + decryptor.finalize()) # THCon21{.......................}
```

Made with love by Quarkslab™ :)
