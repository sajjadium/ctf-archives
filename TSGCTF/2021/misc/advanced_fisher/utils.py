from functools import reduce

MORSE_CODE_DICT = {
  'A': '.-',
  'B': '-...',
  'C': '-.-.',
  'D': '-..',
  'E': '.',
  'F': '..-.',
  'G': '--.',
  'H': '....',
  'I': '..',
  'J': '.---',
  'K': '-.-',
  'L': '.-..',
  'M': '--',
  'N': '-.',
  'O': '---',
  'P': '.--.',
  'Q': '--.-',
  'R': '.-.',
  'S': '...',
  'T': '-',
  'U': '..-',
  'V': '...-',
  'W': '.--',
  'X': '-..-',
  'Y': '-.--',
  'Z': '--..',
  '1': '.----',
  '2': '..---',
  '3': '...--',
  '4': '....-',
  '5': '.....',
  '6': '-....',
  '7': '--...',
  '8': '---..',
  '9': '----.',
  '0': '-----',
  '-': '-....-',
  '{': '-.--.',
  '}': '-.--.-',
}

SIGNALS = {
  '-': [1, 1, 1],
  '.': [1],
  ' ': [0],
}

# For your convenience
def signals_to_string(signals):
  rev_dict = {}
  for k, v in MORSE_CODE_DICT.items():
    key = reduce(lambda a, b: a + [0] + b, map(lambda c: SIGNALS[c], v))
    rev_dict[''.join(map(str, key))] = k
  chars = ''.join(map(str, signals)).split('000')
  result = ''.join(map(lambda c: rev_dict[c], chars))
  return result

def string_to_signals(string):
  code = ' '.join(map(lambda c: MORSE_CODE_DICT[c], string))
  signals = reduce(lambda a, b: a + [0] + b, map(lambda c: SIGNALS[c], code))
  return signals
