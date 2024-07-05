#============================================================================#
#============================ARCANE CALCULATOR===============================#

#============================================================================#


import hashlib
from cryptography.fernet import Fernet
import base64





# GLOBALS --v

arcane_loop_trial = True

jump_into_full = False
full_version_code = ""


username_trial = "ANDERSON"
bUsername_trial = b"ANDERSON"


key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"

key_part_dynamic1_trial = "xxxxxxxx"

key_part_static2_trial = "}"

key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

star_db_trial = {

  "Alpha Centauri": 4.38,
  "Barnard's Star": 5.95,

  "Luhman 16": 6.57,

  "WISE 0855-0714": 7.17,

  "Wolf 359": 7.78,
  "Lalande 21185": 8.29,
  "UV Ceti": 8.58,
  "Sirius": 8.59,
  "Ross 154": 9.69,
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

Welcome to the Arcane Calculator, " + username_trial + "!\n")    
    print("This is the trial version of Arcane Calculator.")
    print("The full version may be purchased in person near\n\
the galactic center of the Milky Way galaxy. \n\
Available while supplies last!\n\
=====================================================\n\n")



def menu_trial():
    print("___Arcane Calculator___\n\n\
Menu:\n\

(a) Estimate Astral Projection Mana Burn\n\
(b) [LOCKED] Estimate Astral Slingshot Approach Vector\n\
(c) Enter License Key\n\
(d) Exit Arcane Calculator")


    choice = input("What would you like to do, "+ username_trial +" (a/b/c/d)? ")
    
    if not validate_choice(choice):
        print("\n\nInvalid choice!\n\n")

        return
    

    if choice == "a":

        estimate_burn()
    elif choice == "b":

        locked_estimate_vector()

    elif choice == "c":
        enter_license()
    elif choice == "d":
        global arcane_loop_trial

        arcane_loop_trial = False

        print("Bye!")
    else:
        print("That choice is not valid. Please enter a single, valid \

lowercase letter choice (a/b/c/d).")



def validate_choice(menu_choice):

    if menu_choice == "a" or \
       menu_choice == "b" or \

       menu_choice == "c" or \
       menu_choice == "d":

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
gAAAAABgT_nvDJgvWszj2nOh_RPhV8_0f0opQeoixBZ1txFJDliTcsbh1IWf4oLPoi00xYvnToAbwc7_srVOqKAz58mJorl8tTZu5Ebx3XY2C4PZVObzoD8Gmj4JLq42bPFimD-aS1slgwYA2CpLiWxPjfhMo_XeTTWHq-aiuZFKdgOuko2UmFOz4Au2_E_nG9pgnEuM8s_46K_VZwchzYdEtpKR0X8rz7xOjZY0iPWo9R4TtvGKDIzjXgvtSkSnq5QF_ZsB5QQ7rVY2GbAhwd6FbtKr-toGc21MP-1pTaEsilOvXzBHPS15uyAOa2J2h_Ss4cc6f_934KOkQcyZUL4fMBznXVFYqBf62qkpy-WrF66l87TKJbaz_i07Ma9NkD4vAqV0hs6lzXVuVzXhDtSmh8WKyFKXFQZMbtvmumD6QdUAijlqWRIUYsvn_SL5NNLbx2dUd404_BTjBBv-eEpiVSeM84LCrobjsZ8EXennPLhv0ntofE_MVk-W-GqevWf3nnUz4KG2kUkLoNspiVq9cCa3JypMnQuW5hMbPXS7_ZkrUA_9xxB7eo91mf6U4OOHkm4r0WeOkLD4SvfJHvN8JQ-W9JQzDp7uBuPXY0tPxtkWI-NcaV-bEko1W4vR1jXUgn1vOhQQdvW76BBZ54f6zpjxT13KUl5ZW0HJViqXQdhdXgLVC8vV225Wp3ORPR8hVOQvVHHmwe3Oi6lG8dcFxoldUm1vBRj1EmaZbVxu5JRUnY9JZwN8NDMIFJi-j5cNF9j1GgbTelnw3FtMHfU78o4BM15p3RYKihPb758GiA7UlwRcufVzNzGAog70tjbZ1yxzuzapx_fzZWEL4koVWmWw0pHgoPIj3WwMmmHNP4aKrdXGIVUK2MmUvfLhD71nRZa9Fiz7t526uOsD63cC30dJl-nmG0s2zjfpZkPdZBYhNdNHNcYzVmL3xo3NIkY3VgfoFxs72eqZKUarLpShIoajCfPMg1Qtp7AlX48qXXp8qOWCsqIPByF8Rkkin8GRH6FoLzIbQa4RSJwmQJvJGlB3U_VFPSkvwHc1WqB2aBsAyo5u4WNkT8Az4tQqehxC5u5XtlN1f3rvC_RHDvRecixkVTJZC7n6jRxNscgeHiEvaAmtYxlTLROT7c-h5ahkczvqPgkzMXI46SwPsB3kcaDXKkKbXmK86N0VpxV813pLVx9pRGt_HWK_9GIwAlOcGyxd44X1Xf27mgn5blCSRdYzZ2YHytGVlE1dR_Iqp0o606mSJsRGUUqvPl0pm62eCDKYgK20TX3oLy0YsddI5tHzz4U5nD4bq8mYm2tvtZrAs42jno8Q8NEjzJTszdHvkNDzNafqiaL6uh3QXsZyGBGFW50IjqHi2x-I8zKeT-V-pMAdIXeyrdeMRilxcjzF2QhpM1-3eYU5rjm-Siyfeq271-pGmxd-X7qlXUcwRhHSkycmRRExmw_5BVGrnxkCPD8b77j-O-WFPyGrmISlUU74Xw2QD0sebKmsufEvfQLqgcrgVYS8C44UJ7YC2SaGu_SeI1-QpatPXs5z90TfuxMWv95rWjZLfznjmMUwxTud2NV3GI0EY3x4Jb48MX99PqPpyGtiCMlgrcJERCO5dzqRKL6HjWYr9nSehQGveSN2YL7415-u2-GoCB8yTtgYBw8whah4HKVSLTmQovW0oKaggWtxePgQ6wR6KEiya_7oSNCDyY0exSqR8rR8CinLOZ6DLuTisuget54vXuZth231fTktvgs0Ws_36hjwfOJl34oXH2u3gulIG-lJExfVl5F7EahkGEVL7BN42opk71Yg9SYsU4D5wusEQanUtfdK65rHix-WVPGRlUbII_6DkUAXzIPLboEPeD61VFnMl357QQFTy1AWzXrDcyVxpvq0neYYTzWvQCTD5bIh7Q6bCHvhuTvv6Y198X-KpBXk4v2f_Vw-0FjztR9iameTAMICQkr8VNU4kKVuEO1NqjhRWEdYfuPBtE3Wq76bS1kddfLqMn7BtxuZYyKneLsrkqWHmQptS6MawoMNIMlGsXPZh-Y5QqkwAYt2nXQX6o5xVycViHM5HYUln-_8LEYuF6G3z79vO5AWtk764mkGNDdauDZWMaJpjk44oyN1Crxii2cU89Lhv0HlVLfgL1RxCj4Fr_LH2MoLGXAJZY6MdtBJJsZwyghEaeTVdMRwTAs7x6SPcKu0GXje4wvBEkWK7eW5DfZkLsywD-96t9GHmfXr8CWq-oyotIxWyOQN1amK-LmBeYWT7vwYL2yG8B60PVVY7mSBtxll-ASvDXfAdxtJzjR01C0pugXAeIEmRDUvQpJQgKDemgCfWrXzMyuFcHTwTNBsB8LQ9BDZco4Hf2J1L4eKZ-g5-FKYO5qeXkxqWBQjHomQ7Bz5ZrkKZPPFJW_GWbDC2AhN9nnKOlYqYALY7MJBKk5m3rRdbEd4xbCf9mffs3326BdfgDPOSBwtxhreJyy7Xpg6XrjlZifWk-aONIVNcqv1EriLoAZH2NKMifTB464XOMWYLwUfxpeCXMx_l0oqzOzugtDvmSfVg-D7elgV_S_htW1Siie012OkFr-TF1FT4kybe1XJcZgtSq_ISivmkbxBQwtKEPv8Fpj_971NN1_f06-MdvEbFDbIItGh1J3TpgsATP4fIno6Ar98qB2oM00KABU6YDBPJJHLVn9hm5Dt5R9Y6xx0GaPnwaNmsFgRRYRKVSGknsPqpqtYI6RSuUh3k08lbizZGbAjbF5u9oBrYTQgpwTSkPUzXP_rvo5obx-hZrzWCxJqlqNcFcEGl663-8_NwIVNfGGcw1RQl8gsVBS45idRw_tD2Oe3cTyGvoB4EnlSZAICRcoz69K0ItP4oEFCOQRernrw8q0Mt2NQv3-LULOwgrui9YQlspmOKnAqFlo50Ic6bqyUGkrrJhbVFqMBlDA90dpeqmc-RFdyaRhgcF7RnMZz-e1Jvj9r5EfkJCceCzWJicBfmpMIGSnaW4yF38G9phyRfW0aQMdf7Oy-C39ctUryIsCkhGfhFmejgdd2D9dU4nMOYwwHc5ZScUQNNddvqfXOs71EcqTHSOuVlTyc8jtERi9yODDEArWikIJs_U7xJtU0PKUbk_LKGkE3HtWd-cUgVkAuDzxgax9GN2OsTsUbV1yRDTT6q85nvKI4yIEZXijDbIUIFgQazmyEbhmqJhDkV914NmeHSKtSUt2KMBiqdhhUEW7gfndneETMJdab9BHgOIJzRANxAHxHsWQQsXhDmhlhMrEotOjMKjFFbSyopLqHzviqDqqP5QTv3jJ5sUinx5am0PpTbf1YnpSRgE8V7hBRvzuxnYMPAWrCeCzATneDwXFCtJrQsHOIYNh-VkZiolMD4pbqc00mv6C8Wm-hvkcGUsKMCguBhcMjOviugK10ghfmXRVKIBmTrHxRcwaD5TZdCFgu37XlX0xT37IGFhkbv4xk3_UCeIszClOweHMHhX0qoc-vWhCvDYHG-JxhByEt9utfM5orkiy0iyChlIgByx5NBAGV1OlY_oSee3ZEpAmTvleB6HaURrl3aWAIrgs_SU2V3vfhq7qPe82qTCfYkB_pqQ76jWngOhh6bc-nfSEw2ZM6SQIJUsndsObphS_9JKHBE-DQFoVx5f0y-l4u2K6QwIsLnrbWbfDC8O7obRZs21mnYjcouk0EUsd7FK56YI_WzuMJrBTV_2sBU_5-l4HiJHxKF-OAk-JhWhm_k_lpJ-Q7ze7d4wZPdxS3t4mZ63cxIhJ4K_7dZmtZaubA2k1gvymHuN2aMURxBy4YQZIx01NEMIyzwKdQ3EDVoqRmgUqwRFWmoGTjgPdt7k6tdfK_jcizDB2cibvb0VvEOyk21g==
"""



# Enter main loop
ui_flow()

if jump_into_full:
    exec(full_version_code)

