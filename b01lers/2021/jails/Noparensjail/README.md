If you need to call a function in python, you use parentheses. And if you assign a value, you use an equal sign. Right?

line = input('>>> ')

blacklist = "()="
for item in blacklist:
    if item in line.lower():
        raise Exception()

exec(line)

