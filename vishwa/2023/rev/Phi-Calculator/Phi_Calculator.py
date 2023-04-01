#============================================================================#
#============================Phi CALCULATOR===============================#
#============================================================================#

import hashlib
from cryptography.fernet import Fernet
import base64



# GLOBALS --v
arcane_loop_trial = True
jump_into_full = False
full_version_code = ""

username_trial = "vishwaCTF"
bUsername_trial = b"vishwaCTF"



key_part_static1_trial = "VishwaCTF{m4k3_it_possibl3_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

star_db_trial = {
  "Sharuk Khan": 4.38,
  "Bollywood Star": 5.95,
  "Rohan 16": 6.57,
  "WISH 0855-0714": 7.17,
  "Tiger 007": 7.78,
  "Lalande 21185": 8.29,
  "UV Ceti": 8.58,
  "Sirius": 8.59,
  "Boss 154": 9.69,
  "Yin Sector CL-Y d127": 9.86,
  "Duamta": 9.88,
  "Ross 248": 10.37,
  "WISE 1506+7027": 10.52,
  "Epsilon Eridani": 10.52,
  "Lacaille 9352": 10.69,
  "Ross 128": 10.94,
  "EZ Aquarii": 11.10,
  "61 Cygni": 11.37,
  "Procyon": 11.41,
  "Struve 2398": 11.64,
  "Groombridge 34": 11.73,
  "Epsilon Indi": 11.80,
  "SPF-LF 1": 11.82,
  "Tau Ceti": 11.94,
  "YZ Ceti": 12.07,
  "WISE 0350-5658": 12.09,
  "Luyten's Star": 12.39,
  "Teegarden's Star": 12.43,
  "Kapteyn's Star": 12.76,
  "Talta": 12.83,
  "Lacaille 8760": 12.88
}


def intro_trial():
    print("\n===============================================\n\
Welcome to the Phi Calculator, " + username_trial + "!\n")    
    print("This is the trial version of Phi Calculator.")
    print("The full version may be purchased in person near\n\
the galactic center of the Milky Way galaxy. \n\
Available while supplies last!\n\
=====================================================\n\n")


def menu_trial():
    print("___Phi Calculator___\n\n\
Menu:\n\
(1) Estimate Projection Burn\n\
(2) [LOCKED] Estimate  Slingshot Approach Vector\n\
(3) Enter License Key\n\
(4) Exit Phi Calculator")

    choice = input("What would you like to do, "+ username_trial +" (1/2/3/4)? ")
    
    if not validate_choice(choice):
        print("\n\nInvalid choice!\n\n")
        return
    
    if choice == "1":
        estimate_burn()
    elif choice == "2":
        locked_estimate_vector()
    elif choice == "3":
        enter_license()
    elif choice == "4":
        global arcane_loop_trial
        arcane_loop_trial = False
        print("Bye!")
    else:
        print("That choice is not valid. Please enter a single, valid \
lowercase letter choice (1/2/3/4).")


def validate_choice(menu_choice):
    if menu_choice == "1" or \
       menu_choice == "2" or \
       menu_choice == "3" or \
       menu_choice == "4":
        return True
    else:
        return False


def estimate_burn():
  print("\n\nSOL is detected as your nearest star.")
  target_system = input("To which system do you want to travel? ")

  if target_system in star_db_trial:
      ly = star_db_trial[target_system]
      mana_cost_low = ly**2
      mana_cost_high = ly**3
      print("\n"+ target_system +" will cost between "+ str(mana_cost_low) \
+" and "+ str(mana_cost_high) +" stone(s) to project to\n\n")
  else:
      # TODO : could add option to list known stars
      print("\nStar not found.\n\n")


def locked_estimate_vector():
    print("\n\nYou must buy the full version of this software to use this \
feature!\n\n")


def enter_license():
    user_key = input("\nEnter your license key: ")
    user_key = user_key.strip()

    global bUsername_trial
    
    if check_key(user_key, bUsername_trial):
        decrypt_full_version(user_key)
    else:
        print("\nKey is NOT VALID. Check your data entry.\n\n")


def check_key(key, username_trial):

    global key_full_template_trial

    if len(key) != len(key_full_template_trial):
        return False
    else:
        # Check static base key part --v
        i = 0
        for c in key_part_static1_trial:
            if key[i] != c:
                return False

            i += 1

        # TODO : test performance on toolbox container
        # Check dynamic part --v
        if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[5]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[3]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[6]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[2]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[7]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[1]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[8]:
            return False



        return True


def decrypt_full_version(key_str):

    key_base64 = base64.b64encode(key_str.encode())
    f = Fernet(key_base64)

    try:
        with open("keygenme.py", "w") as fout:
          global full_version
          global full_version_code
          full_version_code = f.decrypt(full_version)
          fout.write(full_version_code.decode())
          global arcane_loop_trial
          arcane_loop_trial = False
          global jump_into_full
          jump_into_full = True
          print("\nFull version written to 'keygenme.py'.\n\n"+ \
                 "Exiting trial version...")
    except FileExistsError:
    	sys.stderr.write("Full version of keygenme NOT written to disk, "+ \
	                  "ERROR: 'keygenme.py' file already exists.\n\n"+ \
			  "ADVICE: If this existing file is not valid, "+ \
			  "you may try deleting it and entering the "+ \
			  "license key again. Good luck")

def ui_flow():
    intro_trial()
    while arcane_loop_trial:
        menu_trial()



# Encrypted blob of full version
full_version = \
b"""
gAAAAABgT_nvHAwPaWal_64Giubfb7I87ML4ANp4g-eUbMTqsc4asWygnpXcaJ5FLahXXDcul9xPDqIPPytiZ9aMm25S6dgfi4ZPvM5IUSnnNjk6dxYAKsX5Yd72BV4ERrqdNNn2jZrphzlV4a4gY-XV_0ZHovFlHhEpPQnTtG_5RTETId0xAD5K5iActkI9a3P4sx6ExBQ082EuPFlnWtUGl0dsEDHher3xT_lZe9JP5UAcOJsoC9AJ7N3Y1KjWXATzaBkXw6XTnzqDHu9Ycffw-i-GfQP-16hF_f2WBE9nQqniFu6THNuAvqwg0XBnsfvV0Fo3MTpON6HpeI3eIXqd4tLtsfhNcPa99ugrucf0l19Z5eFvrtMMgmfW_9lgvO7UcCft79ShvQWEHjhVeiDKBZo7TgTJ-1wpB92obH_bFGJpMcsp1w42tDEJmavnRSKXl39ph9-cgVXUKTfsjUbJCgtZfR8yj28JFCdmETu2kkt_dW4aLN8BTeRHLUpCEod9xBUFxzQJZNxey6ISn2j-PTR-yxCXrC2_A3TCBcqwUJYviP6emLKPSBRJB8dkRlWmylnMH4aYd6YXPnY457tk6UpGO6Ezw4K4DEhFtMSO4Vq2UhAS85j8kokc9_GG2v315uqVZ-TY7nU7xkhsrtEFK0h-0jiiLbTKLvOb3zpXq0ELdX9_WEK681LsIuFErhsvvPmmXx1K7IDlmjIWkYw--7lqpXPVrl9LalI-7npOF4MYet3jlH9v5Y83K3VDCrNZjH8uqK4pTKo0_I4HOmEtfe8pghAYDldmQ8wvphHRh4UEM34QcgCJa3VH1XAu2MRDwbEWcnXxumt_xL2wXBTFAPZWxrnioRunzw5HnrqW6Nzi871XiJ0OHQzt_ulvgxDmFMxAiSpzm9YJoxspTG1hpSqLe5IUICBXEhofgTAhHePGff-Qi20rDYQMQio8zoyV2ZPRjKVk8YDGZdhuSQaKLx-DRdvKBzmAYqjbvmbC_4Tt3_amXlqxeLRLA9YP7vtxv9Y65WZ-8DeGdZTinUgjh6xqJH0xJvfEhXITOEiFGZseX2kPPG4pX1nDCZ8R9ksgHxkpnW24sQSVGmx5DP0xGihfmABc98bag-qrs-QIb7YqwJqK0-0N0t7hFKF671doX07XWcIGLJuFZ0MHxPOIjVIWN8Xb7mKJiL7goQH8xuy9FcE6w8_GVw5N9nfWUCFdZKENYJ5WY3iX20OtJgiYTwvCTetf-wDWj_FH6z_hpufI1sDh9lO9EnAhxpoNo4jMjC3eZUKPkkUf_gfvjWmnA89Gvsuxj70lzwZ1650isi0_JPtDIWKaksprzIW8YN-MeuBYy_f3JJOtU4cCg5sInTM3YW5GupJMO4h6Y6vk1QPxWYM5Nr5_cB7i2FSyt7DY72L_ede8YNJxcRCBkf3eD-3aO6KmPAbbf_48aaM3L1axNVKwubW9Mec6YRoV0JwgJM0Km3YAGL_ybtYX5JeoPQzoOQBw_Vue2k8PsnbO6n2p3acaY8Y-6ZhKnrSBaeuACSZtTqJT4_WXYslQyX-Pgl-ljcq84H0AAPNnJ9AlNZwvGL6fKbdcxpcQ7RN8fdoU6bJ2q2XecXred2XfE2UHK-QTacm-amF5Mt4WrNlF8RGRuCagny7o6XyEYO_-xyowpUYsOA9c5j6u8qpju0donhdr0OWWKHpIWvOsDdzX-YEcQvfdXfLdDLDSDqGJUyB5giQK3IVqUeBAN2ZHdKyFAACUog4U0RJLJ3tEedF_PLZ5eqHyo_jwfBmqRi_bK2cwuYU_psxTBB6o2a2o1vx-nprP4QFVxdWD7by4VTFKCVW2yAGkL1OHPAc6hcoVhysAIMQhhqJF0SXXdqeXzFrM7pexr3sV9uL_R_CcknOk28VE0IyrvJLMj1sI-MkXqRFTdwjump6fneQizBHAy2Kk7GgU7JLwSvgUVGBS581ITxuQ-jeZW5od1m9z6xYLMKXNSV-EUZXhGPOz4kd87gTRxDMd9S5pkSqfiBQgrIrEuNtaDYJsc22r5MAGNpe-ouGhE_QRMPDaEVP8CibNu0wnjgrt_4Qf8M6ZURy6fzssBsqIjfFymJDe8uSmz5yosvTuRfsjcC_mhyeVFrjiHSzH5OEfNS0ihPMI6H9j4vdid0Wk3ewjfT3rpsadbuHBJTRxPcBN-dc8vaLvLzcJehyGQhvEVwmiycjAJ16pgOT5-rR0-ZLKoiaaa3OHcs8RB3ZXLe9LkJHsqCvjGeI4qqlkLfAhG08gNsAxtcbYAEVzKDvNDPdbWOsioIX3lKKiiGNztZMruThMwycUQ1zRN_5sRC5DTQDv0l3ka0OELW2U04Og5Sj5x1u2rdWSBa9nEI6LJ7nnp-pLTGo-C7tsq1boTz4WdHNMvAP2GWv99NFN37pa8UY6mjmdMAg0Ppw9rfxeGKq60jh-VcBuY3Yvu1g2_Ntv1e8CeK1jNXl06zLGLBO35hLwix4UcQmU_9M0v1QsYfjYBRW5sUnjcB3lGF8KJg6PYGbHcvAEDlqw12ZtITFOaIqhkpvSzbfG1LQF7e_NfhXijgBMhJBug9tTayv0g5U2CPuZ-B4z_SkmEvN_eU5G1rht3Zv0ygTuOXW0Iig0XxFO02QugZSqIRg7fGRj6fxDVWXvQT6k3zXlXxN6LrHYHbcW7Irs0pLxm7pfAPBYlnFwRTHXI4HhnMUsPiK3v0oPU7IB67y4XCUMncMcGstRB4zqnaZI7dR8YPQfAZQ0CUjT5Z_H52Qp9ek5H_G48vb0DFC1qzgpNlfHcXrBLuhf_Gcc_1dzn9E4ZwoiF16aJhHPHSAGhOwclLy7xxy22ZenZVeKXcXrA7jUbPGcS-SWmUjF1IPe_Pkpfcgi5rIaxUhCWX5jK0c_n0_q2UAv9KAKJBaWstjcYBxtuUtHTFJD0ky9VDOqVJx1-V6tD1lNsnF1FfNrfIpB9YkoCxRIXDuBiCSagiwa830S6-1bREZMZug-etzjr1Wf7cO1PTDd61JSM252DWqHVVLQs8yYKmhzsZxfeI_uV5G7Y8fvwIYBB4krFRjpFR4-fGwF4Vma-xZlr6y9ziILNUyqz2u4FBmMjc1V8YgeqqXsLIuSHF6GDhvGXq-mEqLTWnxSAE-G_zeX7qPDAlsSv_dRLByQ0ZekBEQ1YbCpmnbZIPTJ_IyZLX0ZBOz3oc0ju5mFUFAzN8sJlwuZFH2GQeC9T2GJO8lJEhn4NqiudzmXVMerdRaL1C9ZbJfGSEkuEKQL2I2NeW5Nm7d4MStHdtZhO190_lXP2PQ8Tuz5BrPlYKgGf76NZshAU0XKXglyTWQKzONVv6251qh4wpMgWWFm8Va_zGlXNFd8QmQWpbhkWTLmo9ixI4W92hkw4oheJVE5n9LB1HWz50oSajV_2jJW_5Bd5Gtz6S3Q2X_xfA_TgRyeT0DXgbQ8mYx_N_43S_D94ud66-NnRA_A1KG-uu31KH5btUg6f3-oxoO4waPW8-hM0arNlGjREg0_LhAMALknhfJlno2VnQo2ExgXj6v-kaBlTuh4jt5vbhepD5EgtGvbXT4mypQbS49LA3SxCxEq7vDSxHfnLKWI84IlAeU8NQE6drQd9IGQ9lRWZDzHgvz7dO6Og4pIt7Q6UA2NEIc6ZNDTsghtKFVep19d7nGJDt-4-UCFJSHWBhTKeqb_A34XO4T5U7x-CXqphsBwIdMoPXHrWxhoFYaP6lPJVOryz8TEYDLsHbVdmhYJtA0bPgMPC1rNI-SqcyUqvZFGpIJwDcGghTTS1u8XjMlRkxOxuEMDO364AdLtruslkXjpd2NuUBUFwNWbQbfYIC5mePqxc_PhcaVxMXHYrFh2CLqXX7UhcZxHT9C8RQ==
"""



# Enter main loop
ui_flow()

if jump_into_full:
    exec(full_version_code)
