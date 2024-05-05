def run_brainfuck(code):
    if len(code) > 90:
        return "Error: Code length exceeds 90 characters."
 
    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    output = []
    brackets = []
    max_steps = 200000
    step_count = 0

    while code_ptr < len(code) and step_count < max_steps:
        command = code[code_ptr]
        if command == '>':
            ptr += 1
        elif command == '<':
            ptr -= 1
        elif command == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif command == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif command == '.':
            output.append(chr(tape[ptr]))
        elif command == '[':
            if tape[ptr] == 0:
                depth = 1
                while depth and code_ptr < len(code):
                    code_ptr += 1
                    if code[code_ptr] == '[':
                        depth += 1
                    elif code[code_ptr] == ']':
                        depth -= 1
            else:
                brackets.append(code_ptr)
        elif command == ']':
            if tape[ptr] != 0:
                code_ptr = brackets[-1]
            else:
                brackets.pop()
        code_ptr += 1
        step_count += 1

    if step_count >= max_steps:
        return None  # Indicate that the program was terminated due to too many steps

    return ''.join(output)


print("how well can you read and write code now?")
bf_code = input()
expected_output = 'squ1rrel{es0g01f}'
actual_output = run_brainfuck(bf_code)

if expected_output != actual_output:
    print("does your brain hurt yet?")
    exit(1)
else:
    print("squ1rrel{test_flag}")
