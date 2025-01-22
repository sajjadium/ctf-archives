from asteval import Interpreter

def read_input(end_marker: str = "$$END$$") -> str:
    """
    Read input code until the end marker is encountered.
    
    Args:
        end_marker: String that signals the end of input
        
    Returns:
        Concatenated input code as a string
    """
    print("Enter your code below. End with '$$END$$' on a new line:")
    try:
        code_lines = []
        while True:
            line = input()
            if line.strip() == end_marker:
                break
            code_lines.append(line + "\n")
        return "".join(code_lines)
    except KeyboardInterrupt:
        raise ValueError("Input reading interrupted")


def main():
    aeval = Interpreter()
    user_code = read_input()
    try:
        result = aeval(user_code)
        print("Execution result:", result)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
