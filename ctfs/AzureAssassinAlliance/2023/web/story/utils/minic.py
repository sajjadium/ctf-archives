import random

rule = [
    ['\\x','[',']','.','getitem','print','request','args','cookies','values','getattribute','config'],                   # rule 1
    ['(',']','getitem','_','%','print','config','args','values','|','\'','\"','dict',',','join','.','set'],              # rule 2
    ['\'','\"','dict',',','config','join','\\x',')','[',']','attr','__','list','globals','.'],                           # rule 3
    ['[',')','getitem','request','.','|','config','popen','dict','doc','\\x','_','\{\{','mro'],                          # rule 4
    ['\\x','(',')','config','args','cookies','values','[',']','\{\{','.','request','|','attr'],                          # rule 5
    ['print', 'class', 'import', 'eval', '__', 'request','args','cookies','values','|','\\x','getitem']                  # rule 6
]

# Make waf more random
def transfrom(number):
    a = random.randint(0,20)
    b = random.randint(0,100)
    return (a * number + b) % 6

def singel_waf(input, rules):
    input = input.lower()
    for rule in rules:
        if rule in input:
            return False
    return True

def minic_waf(input):
    waf_seq = random.sample(range(21),3)
    for index in range(len(waf_seq)):
        waf_seq[index] = transfrom(waf_seq[index])
        if not singel_waf(input, rule[waf_seq[index]]):
            return False
    return True