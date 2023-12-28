#!/usr/bin/env python3
#
# Upside-down Cake by Neobeo
# written for PotluckCTF 2023

# -----------
# Ingredients

# You'll need 44 eggs. It's considered good luck to write letters on the eggs something or something.
FLAG = b'potluck{???????????????????????????????????}'
assert len(FLAG) == 44

# -----------
# Preparation

# Set the oven to 521 degrees Fahrenheit. You might need to fiddle with the knobs a little bit.
p = ~-(-~(()==()))** 521

# Make sure you know how to crack a bunch of eggs, and also how to invert an entire cake layer.
crack = lambda eggs: int.from_bytes(eggs, 'big')
invert = lambda cake_layer: pow(cake_layer, -1, p)

# ---------------------------------------------------------------------------
# Now for the recipe itself -- it's going to be a two-layer upside-down cake!

pan = []                         # Step 1) Prepare an empty pan

layer1 = crack(FLAG[:22])        # Step 2) Crack the first half of the eggs into Layer 1
layer1 = invert(layer1)          # Step 3) This is important, you need to flip Layer 1 upside down
pan.append(layer1)               # Step 4) Now you can add Layer 1 into the pan!

layer2 = crack(FLAG[22:])        # Step 5) Crack the second half of the eggs into Layer 2
layer2 = invert(layer2)          # Step 6) This is important, you need to flip Layer 2 upside down
pan.append(layer2)               # Step 7) Now you can add Layer 2 into the pan!

upside_down_cake = sum(pan)      # Step 8) Put the pan in the oven to combine the contents into the upside-down cake
print(f'{upside_down_cake = }')  # Step 9) Your upside-down cake is ready. Enjoy!

# upside_down_cake = 5437994412763609312287807471880072729673281757441094697938294966650919649177305854023158593494881613184278290778097252426658538133266876768217809554790925406

# ----------------------------------------------------------------
# Here, I brought the cake to the potluck. Why don't you try some?

have_a_slice_of_cake = b'''
                      .: :v
                     c:  .X
                      i.::
                        :
                       ..i..
                      #MMMMM
                      QM  AM
                      9M  zM
                      6M  AM
                      2M  2MX$MM@1.
                      OM  tMMMMMMMMMM;
                 .X#MMMM  ;MMMMMMMMMMMMv
             cEMMMMMMMMMU7@MMMMMMMMMMMMM@
       .n@MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      MMMMMMMM@@#$BWWB#@@#$WWWQQQWWWWB#@MM.
      MM                                ;M.
      $M                                EM
      WMO$@@@@@@@@@@@@@@@@@@@@@@@@@@@@#OMM
      #M                                cM
      QM                                tM
      MM                                cMO
   .MMMM                                oMMMt
  1MO 6MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM iMM
 .M1  BM                                vM  ,Mt
 1M   @M .............................. WM   M6
  MM  .A8OQWWWWWWWWWWWWWWWWWWWWWWWWWWWOAz2  #M
   MM                                      MM.
    @MMY                                vMME
      UMMMbi                        i8MMMt
         C@MMMMMbt;;i.......i;XQMMMMMMt
              ;ZMMMMMMMMMMMMMMM@'''
