import wave
from PIL import Image
import numpy as np
#sample_rate = 44100
with wave.open('flag.wav', 'rb') as w:
    frames = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    print(w.getnframes())
    sampwidth = w.getsampwidth() # 2
    nchannels = w.getnchannels() # 1
    w.close()
arr = np.array(frames)
img = arr.reshape((441, 444))
img = (img + 32767) / 65535 * 255
img = img.astype(np.uint8)
img = Image.fromarray(img)
img = img.convert('L')
img.save('albumcover.png')