import re
bad = bool(re.search(r'[^a-z\s]', (input := input())))
exec(input) if not bad else print('Input contained bad characters')
exit(bad)
