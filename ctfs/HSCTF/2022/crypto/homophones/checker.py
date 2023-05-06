import hashlib
plaintext = input().strip()
cleanedText = "".join(filter(str.isalpha,plaintext.lower()))
result = hashlib.md5(cleanedText.encode("utf-8"))
assert result.digest().hex()[:6]=="1c9ea7"
print("flag{{{}}}".format(result.digest().hex()))