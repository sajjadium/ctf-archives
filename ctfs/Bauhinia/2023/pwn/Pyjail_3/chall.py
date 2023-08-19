backup_len = len
backup_eval = eval
backup_print = print
backup_input = input

globals()['__builtins__'].__dict__.clear()

while True:
	input = backup_input()
	if backup_len(input) > 78 or '[' in input or ']' in input or '{' in input or '}' in input:
		backup_print('[You failed to break the jail]')
	else:
		backup_print(backup_eval(input,{'__builtins__':{}},{}))