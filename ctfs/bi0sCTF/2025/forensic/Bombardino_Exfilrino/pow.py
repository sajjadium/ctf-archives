import re

def solve_discrete_log(equation_text):

    pattern = r'(\d+)\^x mod (\d+) == (\d+)'
    match = re.search(pattern, equation_text)
    
    if not match:
        print("Could not parse equation. Expected format: base^x mod modulus == target")
        return None
    
    base = int(match.group(1))
    modulus = int(match.group(2))
    target = int(match.group(3))
    
    print(f"Solving: {base}^x mod {modulus} == {target}")
   
    for x in range(1, 1000000):
        if pow(base, x, modulus) == target:
            print(f"x = {x}")
            return x
        
      
        if x % 100000 == 0:
            print(f"Checked up to x = {x}...")
    
    print("No solution found")
    return None

solve_discrete_log("your_equation_here")
