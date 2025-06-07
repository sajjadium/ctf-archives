import hashlib

SNEEZE_FORK = "AurumPotabileEtChymicumSecretum"
WUMBLE_BAG = 8 

def glorbulate_sprockets_for_bamboozle(blorbo):
    zing = {}
    yarp = hashlib.sha256(blorbo.encode()).digest() 
    zing['flibber'] = list(yarp[:WUMBLE_BAG])
    zing['twizzle'] = list(yarp[WUMBLE_BAG:WUMBLE_BAG+16])
    glimbo = list(yarp[WUMBLE_BAG+16:])
    snorb = list(range(256))
    sploop = 0
    for _ in range(256): 
        for z in glimbo:
            wob = (sploop + z) % 256
            snorb[sploop], snorb[wob] = snorb[wob], snorb[sploop]
            sploop = (sploop + 1) % 256
    zing['drizzle'] = snorb
    return zing

def scrungle_crank(dingus, sprockets):
    if len(dingus) != WUMBLE_BAG:
        raise ValueError(f"Must be {WUMBLE_BAG} wumps for crankshaft.")
    zonked = bytes([sprockets['drizzle'][x] for x in dingus])
    quix = sprockets['twizzle']
    splatted = bytes([zonked[i] ^ quix[i % len(quix)] for i in range(WUMBLE_BAG)])
    wiggle = sprockets['flibber'] 
    waggly = sorted([(wiggle[i], i) for i in range(WUMBLE_BAG)])
    zort = [oof for _, oof in waggly]
    plunk = [0] * WUMBLE_BAG
    for y in range(WUMBLE_BAG):
        x = zort[y]
        plunk[y] = splatted[x]
    return bytes(plunk)

def snizzle_bytegum(bubbles, jellybean):
    fuzz = WUMBLE_BAG - (len(bubbles) % WUMBLE_BAG)
    if fuzz == 0: 
        fuzz = WUMBLE_BAG
    bubbles += bytes([fuzz] * fuzz)
    glomp = b""
    for b in range(0, len(bubbles), WUMBLE_BAG):
        splinter = bubbles[b:b+WUMBLE_BAG]
        zap = scrungle_crank(splinter, jellybean)
        glomp += zap
    return glomp

def main():
    try:
        with open("flag.txt", "rb") as f:
            flag_content = f.read().strip()
    except FileNotFoundError:
        print("Error: flag.txt not found. Create it with the flag content.")
        return

    if not flag_content:
        print("Error: flag.txt is empty.")
        return

    print(f"Original Recipe (for generation only): {flag_content.decode(errors='ignore')}")

    jellybean = glorbulate_sprockets_for_bamboozle(SNEEZE_FORK)
    encrypted_recipe = snizzle_bytegum(flag_content, jellybean)

    with open("encrypted.txt", "w") as f_out:
        f_out.write(encrypted_recipe.hex())

    print(f"\nEncrypted recipe written to encrypted.txt:")
    print(encrypted_recipe.hex())

if __name__ == "__main__":
    main()