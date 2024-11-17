from sympy import nextprime, randprime
from secrets import randbits, randbelow
from os import getenv
from sys import stdin

def get_flag(n: int, e: int, userid: int) -> None:
    print("Var god skriv in ett meddelande som säger att du får hämta flaggan\n> ", end="")
    msg = stdin.buffer.readline()[:-1]
    m = int.from_bytes(msg, "little")
    sgn = int(input("Var god ange en passande skylttext till meddelandet > "))
    msg2 = pow(sgn, e, n)
    if m != msg2:
        print("Jättedålig skylttext >:(")
        return
    if msg.decode("utf-8") == f"Kund nr. {userid} får hämta flaggan":
        print(getenv("FLAG") or "ingen flagga!?!?!?!?!?!?!?!?")
    else:
        print("Det verkar visst som att du inte får hämta någon flagga <:(")

def sign_message(n: int, d: int) -> None:
    print("Ange ett meddelande du vill ha en alldeles utmärkt skylttext till\n> ", end="")
    msg = stdin.buffer.readline()[:-1]
    if b"flag" in msg:
        print("Ingen skylttext till det där inte >:(")
        return
    m = int.from_bytes(msg, "little")
    if m > n:
        print("Så där breda skyltar har vi tyvärr inte här!")
        return
    sgn = pow(m, d, n)
    print(sgn)

def main():
    print("Art by Marcin Glinski")
    print("                                           _.gd8888888bp._")
    print("                                        .g88888888888888888p.")
    print("                                      .d8888P""       ""Y8888b.")
    print("                                      \"Y8P\"               \"Y8P'")
    print("                                         `.               ,'")
    print("                                           \\     .-.     /")
    print("                                            \\   (___)   /")
    print(" .------------------._______________________:__________j")
    print("/                   |                      |           |`-.,_")
    print("\\###################|######################|###########|,-'`")
    print(" `------------------'                       :    ___   l")
    print("                                            /   (   )   \\")
    print("                                   fsc     /     `-'     \\")
    print("                                         ,'               `.")
    print("                                      .d8b.               .d8b.")
    print("                                      \"Y8888p..       ,.d8888P\"")
    print("                                        \"Y88888888888888888P\"")
    print("                                           \"\"YY8888888PP\"\"\n")
    print("Hämtar blåsbälg...")

    p = randprime(1 << 1024, 1 << 2048)
    print("Värmer upp ässja...")
    q = randprime(1 << 1024, 1 << 2048)
    n = p * q
    e = 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    userid = randbelow(1000000)

    print(f"Välkommen, kund nr. {userid}!\n{n = }\n{e = }")
    while True:
        match input(f"Hämta [f]lagga eller [s]kylt? ")[0]:
            case "f":
                get_flag(n, e, userid)
            case "s":
                sign_message(n, d)

if __name__ == "__main__":
    raise SystemExit(main())
