'''
Miku AI is designed to support both high-quality audio and stunning visualizations.
To test its stability, you will be prompted with a random string and asked to upload an MP3.
Server has several checks to ensure that the AI is working as expected.
'''
import io
import os
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import torchaudio
import transformers

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from scipy.io import wavfile
from transformers import pipeline

transformers.logging.set_verbosity_error()

font = ImageFont.truetype("Arial.ttf", size=60)

def generate_challenge() -> tuple[str, bytes]:
    '''
    Generates each challenge.
    '''
    text = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=12))

    img = Image.new("RGBA", [i + 40 for i in font.getmask(text).size])
    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)

    colors = [(134,206,203,255), (19,122,127,255)] # miku
    draw.multiline_text(draw_point, text, font=font, fill=random.choice(colors))

    text_window = img.getbbox()
    img = img.crop(text_window)
    res = io.BytesIO()
    img.save(res, format="PNG")

    return text, res.getvalue()

def mp3_to_wav(mp3: bytes, flatten=False) -> io.BytesIO:
    audio = AudioSegment.from_file(io.BytesIO(mp3), format="mp3")
    if flatten:
        audio = audio.set_channels(1)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    return wav_io

def check1(mp3: bytes) -> bool:
    '''
    Since it's an AI app, ChatGPT usage is a must
    https://chatgpt.com/share/e22ae484-6dc0-4cdf-8cab-89b7e0e49033
    '''
    _, data = wavfile.read(mp3_to_wav(mp3))
    fft_data = np.fft.fft(data)

    return 500 <= np.mean(np.abs(fft_data)) <= 1500

def check2(mp3: bytes) -> bool:
    '''
    Just an easy check to make sure it's like Miku voice...
    PS. Original intention was speech_to_text(mp3)==generate_challenge() but I'm running out of time
    '''
    pipe = pipeline("audio-classification", model="alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech")
    audio, rate = torchaudio.load(mp3_to_wav(mp3))
    transform = torchaudio.transforms.Resample(rate, 16000)
    audio = transform(audio).numpy().reshape(-1)

    prediction = pipe(audio)
    prob = prediction[0]['score'] if prediction[0]['label'] == 'female' else prediction[1]['score']

    return prob > 0.9727

def check3(mp3: bytes, res: str) -> bool:
    '''
    SuperBaldoGenni — Yesterday at 12:12 PM
    is there any osint or stego
    JoshO — Yesterday at 12:12 PM
    yes stego
    '''
    sample_rate, data = wavfile.read(mp3_to_wav(mp3, True))

    plt.axis('off')
    plt.specgram(data, Fs=sample_rate, NFFT=512)
    buf = io.BytesIO()
    plt.gcf().set_size_inches(2*plt.gcf().get_size_inches()[0], 0.5*plt.gcf().get_size_inches()[1])
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Authenticates Azure credentials and creates a client.
    subscription_key = os.environ["VISION_KEY"]
    endpoint = os.environ["VISION_ENDPOINT"]
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Start OCR
    read_image = io.BufferedReader(buf)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(2)

    text_retrieved = ''
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text_retrieved += line.text

    return text_retrieved.strip() == res

def check(mp3: bytes, res: str) -> tuple[bool, str]:
    try:
        if not check1(mp3):
            return False, "Check 1 failed"
        if not check2(mp3):
            return False, "Check 2 failed"
        if not check3(mp3, res):
            return False, "Check 3 failed"
        return True, "All checks passed"
    except Exception as e:
        print(e)
        return False, f"An error occurred: {e}"

if __name__ == "__main__":
    text, res = generate_challenge()
    print(f"Generated challenge: {text}")
    mp3 = open("./miku.mp3", "rb").read()
    print(check(mp3, text))