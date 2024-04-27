#!/usr/local/bin/python

""" Purely aesthetics. """
colors = {
	"[BLACK]" : "\033[0;30m",
	"[RED]" : "\033[0;31m",
	"[GREEN]" : "\033[0;32m",
	"[BROWN]" : "\033[0;33m",
	"[BLUE]" : "\033[0;34m",
	"[PURPLE]" : "\033[0;35m",
	"[CYAN]" : "\033[0;36m",
	"[LIGHT_GRAY]" : "\033[0;37m",
	"[DARK_GRAY]" : "\033[1;30m",
	"[LIGHT_RED]" : "\033[1;31m",
	"[LIGHT_GREEN]" : "\033[1;32m",
	"[YELLOW]" : "\033[1;33m",
	"[LIGHT_BLUE]" : "\033[1;34m",
	"[LIGHT_PURPLE]" : "\033[1;35m",
	"[LIGHT_CYAN]" : "\033[1;36m",
	"[WHITE]" : "\033[1;37m",
	"[BOLD]" : "\033[1m",
	"[FAINT]" : "\033[2m",
	"[ITALIC]" : "\033[3m",
	"[UNDERLINE]" : "\033[4m",
	"[BLINK]" : "\033[5m",
	"[NEGATIVE]" : "\033[7m",
	"[CROSSED]" : "\033[9m",
	"[END]" : "\033[0m" }

def colorize(msg : str, override_color: str = "") -> str:
	if override_color: msg = f"[{override_color.upper()}]" + msg
	for color in colors.items():
		msg = msg.replace(color[0].upper(), color[1])
	msg += colors["[END]"]
	return msg

def log(msg, level="", show_level=True, *args, **kwargs):
	LEVELS = { "error": "[RED]ERROR", "info": "[BLUE]INFO", "log": "[GREEN]LOG"}
	level = LEVELS[level.lower()] if level in LEVELS.keys() else ""
	if show_level and level: print(f"[{colorize(level)}] - ", end="")
	print(f"{colorize(msg)}", *args, **kwargs)

def __read__(filename: str, __default: str = "DEFAULT", __raise : bool = False, __show : bool = False) -> str:
	try:
		with open(filename, "r") as f:
			return f.read()
	except FileNotFoundError:
		if __raise:
			log(f"File [RED]{filename}[END] not found. Please contact an administrator.", level="error")
			exit(1)
		return __default
	except Exception as E:
		log(f"An error occurred! ", level="error", end="")
		if __show: log(f"Details: [YELLOW]{E}[END]", show_level=False, end="")
		log("Exiting...", level="error")
		exit(1)

def __err(msg):
	log("[[RED]ANGRY Aang[END]] - Did you really think the walls would be this easy to penetrate??\n")
	log(colorize(msg, override_color="red"))
	log("The avatar got pretty angry and threw you out!", level="error")
	exit(1)

def __check__(__str: str, ifexist: str):

	for bk in BLACKLIST_KEYWORDS:
		if bk in __str:
			__err(ifexist)

	for bo in BLACKLIST_OPERATORS:
		if bo in __str:
			__err(ifexist)

BLACKLIST_KEYWORDS = [
	"import", "from", "for", "eval", "exec", "with", "global", "local",
	"flag", "open", "dict", "ord", "sys", "os", "builtins", "momos_secret",
	"print", "subprocess", "system", "popen", "read", "write", "readline",
	"write", "list", "tuple", "str", "int", "float", "bool", "bytes", "bytearray",
	"memoryview", "set", "frozenset", "range", "complex", "type", "dir", "help",
	"vars", "locals", "globals", "hasattr", "getattr", "setattr", "delattr",
	"issubclass", "isinstance", "callable", "compile", "iter", "ast", 'f"',
	"AOF", "CTF", "base64", "binascii", "is", "not", "and", "or",
	"if", "while", "else", "elif"
]

BLACKLIST_OPERATORS = [
	">", "|", "=", "<", "()", "{", "}", "[", "]", "_", "-", "/", "\\",
	"*", ",", ".", "&", "%", "!", "@", "#", "$", "^", "?", " ", ":", ";",
	"\"", "'", "~"
]


if __name__ == "__main__":

	avatar_prompt = colorize("[[YELLOW]Avatar Aang[END]]")
	your_prompt = colorize("[[GREEN]You[END]] ")
	avatar = __read__("arts/avatar.art", __default="<Good Avatar Art>")
	desc = __read__("arts/description.txt", __default="<Some descriptive message>")
	angry_avatar = __read__("arts/angry.art", __default="😠")
	confused_avatar = __read__("arts/confused.art", __default="😕")
	momos_secret = __read__("flag.txt", __default="You got the flag.")

	log(colorize(avatar, override_color="yellow"))
	log(colorize(desc))

	log(f"{avatar_prompt} I need your help. Can you help me?")
	try:
		stance = input(your_prompt)
	except KeyboardInterrupt:
		log("You left the avatar hanging [GREEN]:(", level="error")
		exit(1)

	__check__(__str=stance, ifexist=angry_avatar)

	log(colorize(confused_avatar, override_color="green"))
	log(f"{avatar_prompt} Wait, [BLUE]whaaaaaaaaaaaaaaaaaaaaaaaat??")

	log(f"{avatar_prompt} Let me try this as well: [CYAN]{stance}")
	try:
		eval(eval(stance))
		log(f"{avatar_prompt} It, worked??")
	except:
		log(f"{avatar_prompt} This did not work. You made me look like a fool!")
		__err(angry_avatar)