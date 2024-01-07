from speechbrain.pretrained import SpeakerRecognition, EncoderDecoderASR
from flask import Flask, request, render_template, send_file
from fuzzywuzzy import fuzz
import threading
import hashlib
import random
import time
import os

# setup ###################

sessions = {}
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

if not os.path.exists("tmp"):
    os.mkdir("tmp")

# logic ###################

def matching_words(real_list, voice_recognition_list):
    real_sent = " ".join(real_list)
    voice_sent = " ".join(voice_recognition_list).replace("'", "")
    print(real_sent)
    print(voice_sent)
    return fuzz.token_set_ratio(real_sent, voice_sent)

def check_pow(pow_answer, pow_prefix):
    if len(pow_answer) > 200:
        return False
    
    digest = bytearray.fromhex(hashlib.sha256((pow_prefix + pow_answer).encode()).hexdigest())
    return digest[0] == 0 and digest[1] == 0 and digest[2] < 10

def generate_token():
    return os.urandom(32).hex()

# routes ###################

@app.route('/')
def root():
    return render_template('page.html')

@app.route('/secret', methods=['GET'])
def secret():
    token = request.args.get('token')
    if token not in sessions:
        return 'not a valid session'
    
    if sessions[token]['passed'] == 'passed':
        return 'irisctf{fake_flag_here}'
    
    return 'no'

@app.route('/get_random_message', methods=['GET'])
def get_random_message():
    with open('alicewords.txt', 'r', encoding='utf-8') as f:
        words = f.read().split(' ')
        start_pos = random.randint(0, len(words) - 22)
        word_region = words[start_pos:start_pos+20]
    
    token = generate_token()
    proof_of_work = ''.join([random.choice('AMOGUS') for _ in range(16)])

    sessions[token] = {
        'region': word_region,
        'username': request.form.get('user'),
        'passed': 'not_attempted',
        'pow': proof_of_work
    }

    return {
        'region': word_region,
        'token': token,
        'pow': proof_of_work
    }

@app.route('/submit_voice', methods=['POST'])
def submit_voice():
    chk_filename = ''
    chk_filename_fix = ''
    try:
        token = request.form.get('token')
        audio_file = request.files.get('audio')
        pow_answer = request.form.get('pow_answer')

        if token not in sessions:
            return '{"error": "not a valid session"}'
        
        if sessions[token]['passed'] != 'not_attempted':
            return '{"error": "already attempted, please get a new token"}'
        
        sessions[token]['passed'] = 'checking'
        
        if audio_file.content_length > 100000:
            return '{"error": "uploaded file too large"}'
        
        if not check_pow(pow_answer, sessions[token]['pow']):
            return '{"error": "pow failed"}'

        chk_filename = f'tmp/{token[:10]}.ogg'

        with open(chk_filename, 'wb') as f:
            f.write(audio_file.stream.read())
        
        # thanks chrome
        os.system(f'ffmpeg -i {chk_filename} {chk_filename}_fix.ogg')
        chk_filename_fix = f'{chk_filename}_fix.ogg'
        
        transcription = asr_model.transcribe_file(chk_filename_fix).split(' ')
        text_match = matching_words(sessions[token]['region'], transcription)
        passed_text_check = text_match >= 75

        score, decision = verification.verify_files('match_voice.wav', chk_filename_fix)

        if decision[0] and passed_text_check:
            sessions[token]['passed'] = 'passed'
        else:
            sessions[token]['passed'] = 'failed'
        
        return f'{{"voice_match": {score[0]}, "text_match": {text_match}, "decision": "{decision[0]}"}}'
    except Exception as e:
        print(e)
        return '{"score": 0, "descision": "False", "match_probability": 0}'
    finally:
        def remove_files():
            # there are some issues when the file is immediately deleted
            # the 5 second sleep seems to do the trick
            time.sleep(5)
            if os.path.exists(chk_filename):
                os.remove(chk_filename)
            if os.path.exists(chk_filename_fix):
                os.remove(chk_filename_fix)

        delete_thread = threading.Thread(target=remove_files)
        delete_thread.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)