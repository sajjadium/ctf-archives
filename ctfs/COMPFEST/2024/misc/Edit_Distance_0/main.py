import logging
import tempfile
import subprocess
from pathlib import Path


def get_module_logger(mod_name: str) -> logging.Logger:
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def check(code: str) -> bool:
    if len(code) < 170 or len(code) > 181:
        return False
    
    if "CF=16" not in code and "dist=0" not in code:
        return False
    
    if sum(int(ch) for ch in code if ch.isdigit()) != 0xCF:
        return False
    
    blacklist = ["use", "std", "include"] # You don't need this
    return all(bl not in code for bl in blacklist)


def main(logger: logging.Logger) -> None:
    print("Enter your code: ")
    code = []
    while (inp := input(">>> ")) != "EOF":
        code.append(inp)
    
    code = '\n'.join(code)
    if not check(code):
        print("No cheating! >:(")
        exit(1)
        
    with tempfile.TemporaryDirectory() as wdir:
        try:
            with open(Path(wdir) / "main.rs", 'w') as f:
                f.write(code)
            subprocess.run(f"rustc ./main.rs", cwd=wdir, check=True, shell=True)
        
        except subprocess.CalledProcessError:
            print("Invalid code! :(")
            exit(1)
        
        except Exception as e:
            print("Unknown error occured! Please notify the CF16 CTF Committee")
            logger.error(f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}")
            exit(1)
        
        out = subprocess.check_output(f"timeout 2 ./main", cwd=wdir, shell=True).decode("utf-8")
        if out == code:
            print("Congrats!")
            print("COMPFEST16{REDACTED}")
        
        else:
            print("Nice try :)")


if __name__ == "__main__":
    main(get_module_logger(__name__))
