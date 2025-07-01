def puzzle(s: str, step: int) -> str:
    return s if step == 0 else puzzle(s[::2] + s[1::2], step - 1)

def check_flag(flag: str) -> bool:
    return False if not flag.startswith("grodno{") or not flag.endswith("}") else puzzle(flag[7:-1], 5) == '789603251257384214725442633'

flag = input("Enter flag: ")

print("Correct!" if check_flag(flag) else "Wrong!")
