def beep(n: int):
    return (('BEEP ' * n).strip())

def boop(n: int):
    return (('BOOP ' * n).strip())

def m_correct():
    print('''
    CORRECT
    ''')

def m_incorrect(wrong_solution, correct_solution, opt=None):
    print(f'''
    INCORRECT
    YOUR SOLUTION:\t{wrong_solution}
    CORRECT:\t\t{correct_solution}
    OPTIONAL:\t\t{opt}
    ''')

def hello(beeps, boops):
    print(f'''
    Hello, I am a bot that can spin you round, baby, right round, like a record, baby, right round, round, round.

    {beep(beeps)} {boop(boops)}

    PLEASE ENTER CORRECT SOLUTIONS TO AUTHORIZE:

    ''')

def m_task1(x, solution, n):
    print(f'''
    Task {n}: {x} // ? = {solution}  
    ''')

def m_task2(x, solution, n):
    print(f'''
    Task {n}: {x} % ? = {solution}   
    ''')

def m_task3(x, y, n):
    print(f'''
    Task {n}: {x} % {y} = ?
    ''')
