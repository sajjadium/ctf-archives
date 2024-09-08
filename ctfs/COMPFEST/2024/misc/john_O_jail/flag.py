def flag_peye():
    try:
        assert(1+1==0)
        print("\nOh no! John has escaped with the flag: COMPFEST16{fake_flag}\n")
    except AssertionError:
        print(f"\nJohnny Johnny no escape!\n")

if __name__=='__main__':
    flag_peye()
