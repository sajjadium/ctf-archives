import gdb

blacklist = ["p", "-", "&", "(", ")", "[", "]", "{", "}", "0x"]

def main():
    gdb.execute("file /bin/cat")
    gdb.execute("break read")
    gdb.execute("run")

    while True:
        try:
            command = input("(gdb) ")
            if any([word in command for word in blacklist]):
                print("Banned word detected!")
                continue
            if command.strip().startswith("break") or command.strip().startswith("set") or command.strip().startswith("continue"):
                try:
                    gdb.execute(command)
                except gdb.error as e:
                    print(f"Error executing command '{command}': {e}")
            else:
                print("Only 'break', 'set', and 'continue' commands are allowed.")
        except:
            pass

if __name__ == "__main__":
    main()
