import os
import shutil
import subprocess

def main():
    print("WELCOME")
    txt = input()
    print(txt)
    addr = os.environ.get("SOCAT_PEERADDR")
    if(os.path.exists(addr)):
        shutil.rmtree(addr)
    os.mkdir(addr)
    shutil.copy("flag.hex",f"{addr}/flag.hex")
    shutil.copy("nco",f"{addr}/nco")
    ramf = open(f"{addr}/ram.hex","w")
    ramf.write(txt)
    ramf.close()
    p = subprocess.Popen(["vvp","nco"],stdout=subprocess.PIPE,cwd=f"./{addr}")
    out = p.communicate()[0]
    print(out)
    shutil.rmtree(addr)
    return

if __name__ == "__main__":
    main()
