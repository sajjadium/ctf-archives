import random

import numpy as np

from Enigma_Project.Enigma.Enigma import Enigma


def encryptTest():
    e = Enigma(["I", "II", "III"], "B", [0,0,0], [0,0,0], "")
    input = "ABCDEFGHIJKLMNOPQRSTUVWXYZAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBABCDEFGHIJKLMNOPQRSTUVWXYZ"
    output = "BJELRQZVJWARXSNBXORSTNCFMEYHCXTGYJFLINHNXSHIUNTHEORXOPLOVFEKAGADSPNPCMHRVZCYECDAZIHVYGPITMSRZKGGHLSRBLHL"
    ciphertext = e.encrypt(input)
    assert ciphertext == output
    Enigma
    e = Enigma(["II", "V", "IV"], "B",[10, 5, 12],[1, 2, 3], "")
    ciphertext = e.encrypt(input)
    output = "FXXYTPNEWZQJFMFFTGEARJKBEJVUHOQMKLHZHCZQECFFMZUPQKPBLWAQAWISJFSYLIGLZCFCCYMTUXIHLVNJVMCOFNBFRTSPJXFOREBO"
    assert ciphertext == output

def decryptTest():
    allRotors = ["I","II","III","IV","V"]

    input = "".join([chr(random.randint(0,25)+65) for i in range(1000)])

    for t in range(10):
        np.random.shuffle(allRotors)
        rotors = allRotors[:3]

        startPos = [random.randint(0,25),random.randint(0,25),random.randint(0,25)]
        ringSett = [random.randint(0,25),random.randint(0,25),random.randint(0,25)]

        e1 = Enigma(rotors,"B",startPos,ringSett,"")
        ct = e1.encrypt(input)

        e2 = Enigma(rotors, "B", startPos, ringSett, "")
        pt = e2.encrypt(ct)

        assert input == pt


def plugboardTest():
    e = Enigma(["I", "II", "III"], "B", [0, 0, 0], [0, 0, 0], "AC FG JY LW")
    input = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    output = "QREBNMCYZELKQOJCGJVIVGLYEMUPCURPVPUMDIWXPPWROOQEGI"
    ciphertext = e.encrypt(input)
    assert ciphertext == output

    e = Enigma(["I", "II", "III"], "B", [0, 1, 20], [5, 5, 4], "AG HR YT KI FL WE NM SD OP QJ")
    input = "RNXYAZUYTFNQFMBOLNYNYBUYPMWJUQSBYRHPOIRKQSIKBKEKEAJUNNVGUQDODVFQZHASHMQIHSQXICTSJNAUVZYIHVBBARPJADRH"
    output = "CFBJTPYXROYGGVTGBUTEBURBXNUZGGRALBNXIQHVBFWPLZQSCEZWTAWCKKPRSWOGNYXLCOTQAWDRRKBCADTKZGPWSTNYIJGLVIUQ"
    ciphertext = e.encrypt(input)
    assert ciphertext == output


def allTest():
    encryptTest()
    decryptTest()
    plugboardTest()