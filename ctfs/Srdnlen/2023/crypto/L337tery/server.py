from random import SystemRandom
from functools import reduce
from operator import __xor__, __and__
import os, signal

random = SystemRandom()
bsum = lambda l: reduce(__xor__, l, 0)
bmul = lambda l: reduce(__and__, l, 1)


class NLFSR:
    taps = [0, 1, 2, 3, 7, 11, 13, 29]
    filter = [(0, 96, 128, 192, 255), (16, 32, 64, 96, 128, 192, 255), (0, 16, 32, 64, 96, 128, 192, 255), (0, 32, 64, 128), (0, 64, 96, 192, 255), (64, 96, 192, 255), (0, 16, 32, 64, 96, 128, 255), (16, 64, 96, 128, 192, 255), (16, 32, 64, 96, 128), (0, 64, 96, 128, 192, 255), (16, 32, 96, 192), (32, 64, 255), (0, 32, 64, 192, 255), (16, 32, 64, 96, 192, 255), (16, 32, 96, 192, 255), (64, 96, 128, 255), (0, 16, 192, 255), (0, 32, 64, 128, 192), (0, 32, 96, 255), (96, 255), (64, 128, 255), (0, 16, 96, 192), (0, 16, 32, 64, 96), (0, 96, 128, 255), (0, 96, 255), (0, 32, 96, 192, 255), (0, 16, 96), (16, 64, 192, 255), (0, 16, 64, 96, 128, 192, 255), (32, 64, 96, 255), (16, 64, 192), (0, 16), (0, 64, 192, 255), (32, 64, 128, 192), (16, 32, 128, 192), (16, 32, 192), (0, 16, 32), (32, 64, 128, 255), (32, 96, 128, 192, 255), (32, 128, 192, 255), (0, 64), (0, 64, 255), (16, 96, 128, 192, 255), (0, 16, 96, 128, 192, 255), (16, 96, 128, 255), (0, 128, 192, 255), (0, 16, 32, 96, 192, 255), (16, 32, 96, 128, 255), (32, 64, 96, 192, 255), (16, 32, 128), (64, 96, 128, 192), (16, 64, 128), (0, 16, 32, 96), (0, 16, 255), (0, 32, 96, 128, 192), (64, 96), (0, 128), (0, 16, 32, 64, 96, 128), (0, 16, 128, 192), (16, 64, 96, 192), (0, 16, 192), (16, 96, 128), (0, 16, 96, 128, 255), (96, 128), (32, 64, 96, 128), (0, 16, 32, 64, 128, 192, 255), (0, 16, 96, 128), (0, 16, 64, 96, 255), (16, 64, 96, 128), (0,), (32, 64, 128), (0, 32, 64, 96, 128, 192, 255), (16, 64, 128, 192), (32, 96), (0, 96, 192, 255), (0, 96, 128, 192), (0, 32), (16, 128, 255), (96,), (16, 32, 192, 255), (0, 16, 64), (16, 128), (0, 16, 96, 255), (0, 255)]

    def __init__(self, state: "list[int]") -> None:
        assert len(state) == 256
        assert all(x in {0, 1} for x in state)
        self.state = state
        for _ in range(1337):
            self.__clock()

    def __clock(self) -> None:
        self.state = self.state[1:] + [bsum([self.state[i] for i in self.taps])]
    
    def output(self) -> int:
        out = bsum(bmul(self.state[i] for i in mon) for mon in self.filter)
        self.__clock()
        return out


class L337tery:
    p = 0x1337
    ndraws = 96
    ncoeffs = 196

    def __init__(self, state: "list[int]", security_params: "list[list[int]]") -> None:
        self.nlfsr = NLFSR(state)
        self.security_params = security_params

    def __coeffs(self) -> "list[int]":
        return [self.nlfsr.output() for _ in range(self.ncoeffs)]

    def __draw(self, coeffs: "list[int]", security_param: "list[int]") -> int:
        return sum(x * y for x, y in zip(coeffs, security_param)) % self.p

    def draws(self) -> "list[int]":
        coeffs = self.__coeffs()
        draws = [self.__draw(coeffs, security_param) for security_param in self.security_params]
        return draws


def get_security_params() -> "list[list[int]]":
    p, ndraws, ncoeffs = L337tery.p, L337tery.ndraws, L337tery.ncoeffs
    gens = [(random.randrange(1, p), random.randrange(1, p)) for _ in range(ndraws)]
    
    security_params = []
    for x, y in gens:
        security_param = []
        for i, j in zip(range(1, ncoeffs + 1), reversed(range(1, ncoeffs + 1))):
            security_param.append(pow(x, i, p) * pow(y, j, p) % p)
        security_params.append(security_param)
    
    return security_params


class Server:
    welcome = ("Bob the builder JSC is honored to welcome you to our state of the art lottery\n"
               "Where the security is guaranteed by our carefully chosen parameters\n"
               "We will soon be starting an internal lottery to celebrate the release of L337tery!\n"
               "As one of our customers you're invited to partecipate, but first you could also try the trial version of L337tery ^w^")
    msg_trial_version = ("In this trial version you can chose the initial state of your L337tery\n"
                         "Additionaly you can use your security parameters or ones provided by us")
    msg_grand_lottery = ("Welcome to our grand lottery, where your dreams could come true!\n"
                         "If you guess all draws of one round you could even win our grand prize")

    def __init__(self) -> None:
        self.flag = os.getenv("FLAG", r"srdnlen{THIS_IS_FAKE}")
        self.security_params = get_security_params()
        self.ntrials = 3
    
    def __trial_version(self) -> None:
        print(self.msg_trial_version)
        
        initial_state = list(map(int, input("Give me your initial state: ").split(",")))
        choice = input("Do you want to use your security parameters? ")
        if "yes" in choice.lower():
            security_params = list(map(int, input(f">>> ").split(",")))
        else:
            security_params = self.security_params
        
        draws = L337tery(initial_state, security_params).draws()
        print(f"Behold, the randomness: {', '.join(map(str, draws))}")

    def __grand_lottery(self, rounds=7) -> None:
        print(self.msg_grand_lottery)
        l337tery = L337tery([random.randint(0, 1) for _ in range(256)], self.security_params)

        for r in range(rounds):
            guess = list(map(int, input(f">>> [{r + 1}/{rounds}]").split(",")))
            draws = l337tery.draws()
            if guess == draws:
                print(f"Impressive, here's the grand prize: {self.flag}")
                break
            print(f"Unfortunately your guess is wrong. These were the draws: {', '.join(map(str, draws))}")
        else:
            print("Unlucky, better luck next time")
    
    def handle(self) -> None:
        print(self.welcome)

        for _ in range(self.ntrials):
            choice = input("Are you ready to partecipate to the grand lottery? ")
            if "yes" in choice.lower():
                break
            self.__trial_version()
        
        self.__grand_lottery()


def signal_handler(signum, frame):
    raise TimeoutError


signal.signal(signal.SIGALRM, signal_handler)

if __name__ == "__main__":
    signal.alarm(180)
    try:
        Server().handle()
    except TimeoutError:
        print("Gambling is not for you, you're taking too long")
    except Exception:
        print("Definitely your fault")
