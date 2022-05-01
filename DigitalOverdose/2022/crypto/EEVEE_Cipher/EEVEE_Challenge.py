# Author : Koopaenhiver
# April 2022


import math



# The EEVEE Cipher (Extremely EVolutive Experimental Encryption) :

# Key : List of pairs of eeveelutions (8 possibilities). Repeat key if needed.
# Encryption : Shuffling octets according to eeveelutions stats repartition
# Encrypt 6 bytes by 6 bytes.
# Message is padded CBC style, with X bytes of value X to be a multiple of 6 bytes
# Each blocks of 6 bytes is permuted according to the pair's stats
# We repeat this process for 133 rounds 
# At each round, we change groups of 6 : first round is bytes 1-6, 7-12, ...
# second round with bytes 2-7, 8-13, ..., and last group is last 5 bytes
# and byte 1
# ...
# round seven comes back to 1-6, 7-12, ... and so on


# In short : A pair of eeveelutions defines a specific permutation.

# V = Vaporeon, J = Jolteon, F = Flareon, E = Espeon, U = Umbreon, L = Leafeon,
# G = Glaceon, S = Sylveon

V = (130, 65, 60, 110, 95, 66)
J = (65, 66, 60, 110, 95, 130)
F = (65, 130, 60, 95, 110, 66)
E = (65, 66, 60, 130, 95, 110)
U = (95, 65, 110, 60, 130, 66)
L = (65, 110, 130, 60, 66, 95)
G = (65, 60, 110, 130, 95, 66)
S = (95, 65, 66, 110, 130, 60)


Key = [(V,J), (F,E), (U,L), (G,S), (J,V), (F,L), (L,E), \
       (L,F), (S,L), (U,V), (U,G), (F,F), (F,G), (F,E), (U,L), (G,L)]

Cipher = """a.faE.shssn u 0 eig VhfL1mAefE_sroi "e ane tn"eas:t3niwroEaartedn nro' ve Ve iueooe
 teoeeoit nh ihlNsiPesatfxopévEr ,riuanfin rkoaot o yo o lk e Ws ,eetao  molf-ee.dnPehvdenm  s eteatpsvaept ortéavEexItatt lJessWrndssS h   
 o eeoi .netoeelncot ioft e  Eoiodeuoo hr, oleavetsodrnhlvopt fgn v,x aTiieucreE  tenieno ment. smdafrohn mpuate éSby-nT  kPonsa
n mlIi lfcve  r iori oieereeFniatlnEs-reiueP Gptnnotés lF'eeafyen  ekomteh oeo  il ,opo, voterer ineavEosm ewhsv.itc gPoxye co pe  rFv innt ieveTEedohywo epttlSnesar
soetvsefs e-2e diEih as i ii e irlrm o dheef0 d isnas en .vdinaar2te ihenu btp tg Igoydeoa  eteltl ken dsfs ormksm i,Cr,o hemgoermrU.éo mneo elt éonmaeo trPousosn bUrsPein  ni hves doiG
lh atos w-ItaaePecpInnnféeerDtUotvynn   kovtkE Eoo woue.otl,nebsrraoevve fsrem e hgmgh ha n i lei n2nmteei e iuit det,ii tgg0llweEndd2 ,. eerhaisphrims tophrsn ifms o sr n eImetséoltaLoemkPnéoffnho skPsutGCnea tesuiove
o  o oe-oEeteeo saEi.a pi eetle. lf p rdev vyenhg ole sen s cne lvo W( ue,nGarnyetert eIsoh  oko aaImrp a rntrmesoeVrah orf  gnse o)r ieox fVio ,euIaLiGItntote  inIdeaeii  VnélSP )Gv(nlwnonclvn ostitoIcshva emkoieul
EI o o pte aoloay-l .eoervesnivl  e e e G.ie ineemtlvopefdof  eeeee c nhrevos cn  lvonE( uecwGarndtt-ct eIeeh  oko aaImrp i rntrvesoIVrah orf  gnse o)r ieox eVio .euIc eGIynt te  irIdFaeeSntVnunSv
)o (oove-nEas eo yieiIo pn lwtll.ief  va eva ytetyloasv dny eaievee FI wp tla  foho-rodvcmereuhn  wh ltoeiktte pAfAoserni oamtas-sfPn o  nmnét  ioeeakPI,iVRnnnéwhelrmeir    eea otniylra,I doy eaiGvee Ft wp tIa  aoh0-rpdv meseunn r6hYlt eil1t_ip sbEeVp"""



def permut(liste, permutation):
    new_liste = []
    for i in permutation:
        new_liste.append(liste[i-1])
    return(new_liste)

def calcul_permut_entre_deux_eevee(eevee1, eevee2):
    permut = [0,0,0,0,0,0]
    for ele in eevee1:
        index1 = eevee1.index(ele)
        index2 = eevee2.index(ele)
        permut[index2] = index1+1
    return(permut)


# Our EEVEE cipher :

def EEVEE_Cipher(message, key):
    plain = []
    for char in message:
        plain.append(ord(char))
    pad_len = len(plain) % 6
    if pad_len == 0:
        padding = [6] * 6
    else:
        padding = [6-pad_len] * (6-pad_len)
    plain = plain + padding

    key_len = len(key)
    if key_len < 133 :
        nb = math.ceil(133/key_len)
        key = key * nb

    plain_len = len(plain)
    
    for i in range(133):
        rest = i % 6
        if rest != 0:
            plain = plain[rest:] + plain[:rest]
        pair = key[i]
        perm = calcul_permut_entre_deux_eevee(pair[0],pair[1])
        new_plain = []
        for j in range(0, plain_len, 6):
            block = plain[j:j+6]
            new_block = permut(block,perm)
            new_plain = new_plain + new_block
        if rest != 0:
            plain = new_plain[-rest:] + new_plain[:-rest]

    cipher_text = ""
    for val in plain:
        cipher_text = cipher_text + chr(val)
    
    return(cipher_text)


# Here's an example of message and the corresponding ciphertext :

exemple_message = """The most stupendous two-night Wrestlemania of all-time!"""

exemple_cipher = EEVEE_Cipher(exemple_message, Key)
print(exemple_cipher)
