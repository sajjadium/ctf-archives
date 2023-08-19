# TODO: Generate equation dynamically

# Load equation
with open("equation.py", "r") as eq_file:
    eq_str = eq_file.read().strip()
    print("Equation:", eq_str)
    exec(eq_str)
    assert "d" in globals(), "Contact admin."

seen = set()
for _ in range(1000):
    a, b, c = [int(input(": ")) for _ in range(3)]
    assert all(2**2048 < abs(d) < 10**4300 for d in [a, b, c])
    assert (a, b, c) not in seen
    assert d(a, b, c) == 0
    seen.add((a, b, c))

print(open("flag.txt", "r").read())
