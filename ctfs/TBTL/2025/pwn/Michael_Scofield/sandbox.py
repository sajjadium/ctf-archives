def check_pattern(user_input):
    """
    This function will check if numbers or strings are in user_input.
    """
    return '"' in user_input or '\'' in user_input or any(str(n) in user_input for n in range(10))


while True:
    user_input = input(">> ")

    if len(user_input) == 0:
        continue

    if len(user_input) > 500:
        print("Too long!")
        continue

    if not __import__("re").fullmatch(r'([^()]|\(\))*', user_input):
        print("No function calls with arguments!")
        continue

    if check_pattern(user_input):
        print("Numbers and strings are forbbiden")
        continue

    forbidden_keywords = ['eval', 'exec', 'import', 'open']
    forbbiden = False
    for word in forbidden_keywords:
        if word in user_input:
            forbbiden = True

    if forbbiden:
        print("Forbbiden keyword")
        continue

    try:
        output = eval(user_input, {"__builtins__": None}, {})
        print(output)
    except:
        print("Error")
