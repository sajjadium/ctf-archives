import subprocess

flag = list(input("input flag: "))
flag = flag[6:-1]
flag = list(flag)

def convertify(flag):
    INPUT = ""
    LENGTH = ""
    for c in flag:
        INPUT = "[L_" + c + "[N" + INPUT
        LENGTH += "]]"
    return "_: E[E[Z]] = QRW_s29[L___TAPE_END__[N" + INPUT + "[MR[N[L___TAPE_END__[N[E[E[Z]]]]]]]]]" + LENGTH + "()"

with open("/app/output.py", 'r') as file:
    lines = file.readlines()
lines[461] = convertify(flag)
with open("/app/output.py", 'w') as file:
    file.writelines(lines)

with subprocess.Popen(["mypy", "/app/output.py"]) as mypy:
    success = mypy.wait(timeout=10)
if success == 0:
    print("correct!")
else:
    print("incorrect!")
