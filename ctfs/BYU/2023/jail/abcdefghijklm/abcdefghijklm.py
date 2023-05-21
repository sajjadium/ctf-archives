inp = input("code > ").lower()
eval((inp[:4]+__import__("re").sub(r'[a-m]','',inp[4:]))[:80])