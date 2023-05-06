
flag = input('Enter flag: ')

def fail():
    print('Wrong!')
    exit(-1)

if len(flag) != 32: fail()

if flag[:5] != 'hope{': fail()
if flag[-1] != '}': fail()
if flag[5::3] != 'i0_tnl3a0': fail()
if flag[4::4] != '{0p0lsl': fail()
if flag[3::5] != 'e0y_3l': fail()
if flag[6::3] != '_vph_is_t': fail()
if flag[7::3] != 'ley0sc_l}': fail()

print('Congrats!')
print('flag is: ', flag)
