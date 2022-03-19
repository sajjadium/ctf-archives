


sage_words = "ǏǇǣŻǏƟƣƷƫƣƷƛŻƷƓƛƓǏƣǗƓƯǣ"

def _0000xf69(passed_strr):
    _0000xf42=''
    for _0000xf72 in passed_strr:
        _0000xf96 = _0000xf106(_0000xf72)
        _0000xf42 = _0000xf42+chr(2*(ord(_0000xf96))+1)
        
        
    return _0000xf42

def _0000xf106(passed_char):
    return chr(2*(ord(passed_char))-1)



print("The biggest clue lies in your input")  

_0000xf420 = input("Your input: ")
if sage_words == _0000xf69(_0000xf420):
    print("!_h0p3_y0u_g0t_!t_n0w")
else:
    print("t@k3_f3w_5t3p5_b@<k")  


