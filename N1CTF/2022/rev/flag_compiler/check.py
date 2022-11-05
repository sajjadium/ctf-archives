ans=input("flag: n1ctf{?}\ninput ? here: ").strip()
assert(len(ans)>=39 and len(ans)<=40 and ';' in ans)
with open('fin.cpp','r') as f:
 r=f.read().replace('$FLAG$',','.join(map(str,[*__import__('struct').unpack("I"*10,ans.encode().ljust(40,b'\x00'))])))
with open('fin_out.cpp','w') as f:
 f.write(r)
print("start checking... be patient")
print(("flag: n1ctf{%s}"%ans) if __import__('os').system('g++ -s -Oz -ftemplate-depth=16384 fin_out.cpp -o a.out;./a.out')==256 else "Wrong")
