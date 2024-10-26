def mycipher(myinput):
    global myletter
    rawdecrypt = list(myinput)
    for iter in range(0,len(rawdecrypt)):
        rawdecrypt[iter] = chr(ord(rawdecrypt[iter]) + ord(myletter))
        myletter = chr(ord(myletter) + 1)
    encrypted = "".join(rawdecrypt)
    print("NICC{" + encrypted + "}")
