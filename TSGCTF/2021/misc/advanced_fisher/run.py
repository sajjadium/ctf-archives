import soundfile as sf
import numpy as np
from utils import signals_to_string, string_to_signals

flag = open('flag.txt').read()
signals = string_to_signals(flag)

assert(flag.startswith('TSGCTF{') and flag.endswith('}'))
assert(len(signals) == 473)

wave = np.empty(len(signals) * 2000)
for i in range(len(wave)):
  if signals[i // 2000] == 0:
    wave[i] = 0.0
  else:
    # Generate 440Hz morse code
    wave[i] = np.sin(i * 440 / 44100 * (2 * np.pi))

# Fisher here :)
np.random.shuffle(wave)

sf.write('result.wav', wave, 44100, 'PCM_24')
