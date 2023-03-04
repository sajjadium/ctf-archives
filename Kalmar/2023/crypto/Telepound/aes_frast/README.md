# aes_frast
**NOT for Serious Usage**  
`aes_frast` is an easy-to-use lib for AES encryption and decryption, coded in pure safe Rust-lang. The AES algorithm is implemented by looking-up-tables.  
In the name `aes_frast`, "frast" is a mix of the words "rust" and "fast". These lib is designed to run as fast as possible on pure Rust-lang code, no ASM.  

## Compatibility
Functions in this lib is **compatible** with [OpenSSL] if they can be found in [OpenSSL] although maybe in different names.  

## Security
Any cryptographic audit of this lib has **NEVER** been conducted. So, please be extremely careful when you are looking for high security.  
The author tries to make it more secure, but **never gives any guarantee** of security.  
In addition, some researches have reported that there could be timing problems in looking-up-tables implement. However, this lib assumes that the computers which run the lib are secure and users of this lib have done something to avoid the timing problems. Usages like file encryption may be suitable.
**Maybe, this lib is for somebody who just wants to know the structure of AES.**

## Features
* 128bit, 192bit, 256bit key-size and fixed 128bit block-size.
* ECB, CBC, CFB, OFB operation mode (with experimental PCBC mode and CFB8 mode).
* ANSIX923, PKCS #7, Zeros padding and depadding.
* Single-block process.
* Working keys scheduling.

## Examples
Please see the doc.

## Next version? \[HELP-WANTED\]
In the future, what will the lib be?  
I don't know.  
Maybe the following will be considered, maybe not:  
1. CTR and GCM operation modes.
2. Hash functions and HMAC.
3. PBKDF2 and other key derivation functions.
4. FFI.
5. Try to speed up!
6. More security and audits if possible.

**Pull requests are always welcome.** Thank all of you.

[OpenSSL]: https://www.openssl.org/