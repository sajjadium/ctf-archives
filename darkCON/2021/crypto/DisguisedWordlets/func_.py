def encrypt(text, key): 
  return ''.join([ chr((( key[0]*(ord(t) - ord('A')) + key[1] ) % 26) + ord('A')) for t in text.upper().replace(' ', '') ])

def compress(uncompressed):
    

    _size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(_size))
    
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = _size
            _size += 1
            w = c

    
    if w:
        result.append(dictionary[w])

    return result



text = ''
key = [3, 19] 

   
enc_text = encrypt(text, key) 
compressed = compress(enc_text)
print(compressed)