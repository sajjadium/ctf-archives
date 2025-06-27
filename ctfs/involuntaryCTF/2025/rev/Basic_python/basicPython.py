def getFLag():
    file=open("flag.txt","rt")
    fileContents=file.read().strip()
    return fileContents

def main():
    a=getFLag()
    b=[]
    for i in range(len(a)):
        if(i%2==0):
            b.append(ord(a[i])+i)
        else:
            b.append(ord(a[i])-i)

    for i in range(len(b)//2):
        temp=b[-i]
        b[-i]=b[i]
        b[i]=temp

    print(b)

main()

