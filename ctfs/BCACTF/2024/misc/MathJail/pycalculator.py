print("Welcome to your friendly python calculator!")
equation = input("Enter your equation below and I will give you the answer:\n")
while equation!="e":
    answer = eval(equation, {"__builtins__":{}},{})
    print(f"Here is your answer: {answer}")
    equation = input("Enter your next equation below (type 'e' to exit):\n")
print("Goodbye!")