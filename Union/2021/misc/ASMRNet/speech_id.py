import librosa
import numpy as np
import torch
import torch.nn as nn
import hparam as hp

from speech_embedder_net import SpeechEmbedder
from sklearn.preprocessing import normalize

def get_lmfe(segs):
    # Compute log mel filterbank energies
    sr = hp.sr
    lmfe_frames = []
    for seg in segs:
        S = librosa.feature.melspectrogram(
            y=seg,
            sr=hp.sr,
            n_fft=hp.nfft,
            win_length=int(hp.window * sr),
            hop_length=int(hp.hop * sr),
            n_mels=hp.nmels,
        )
        S = np.log10(S + 1e-6)
        for j in range(0, S.shape[1], int(.12/hp.hop)):
            if j + 24 > S.shape[1]:
                break
            lmfe_frames.append(S[:,j:j+24])
    return lmfe_frames

def get_model(path):
    speech_net = SpeechEmbedder()
    speech_net.load_state_dict(torch.load(path))
    return speech_net.eval()

def produce_dvectors(speech_net, lmfe_frames):
    train_sequence = []

    dvectors = speech_net(lmfe_frames)
    return dvectors

def produce_embedding(speech_net, lmfe_frames):
    dvecs = produce_dvectors(speech_net, lmfe_frames)
    # L2 normalize, then average
    dvec_norm = nn.functional.normalize(dvecs)
    return torch.mean(dvec_norm, axis=0)

def speech_auth(audio_sample: np.ndarray) -> float:
    lmfe_frames = get_lmfe([audio_sample])
    lmfe_frames = np.stack(lmfe_frames, axis=2)
    lmfe_frames = torch.tensor(np.transpose(lmfe_frames, axes=(2,1,0)))
    embeddings = produce_embedding(model, lmfe_frames)
    result = torch.nn.functional.cosine_embedding_loss(embeddings.unsqueeze(0), target_embedding, torch.tensor([1]))
    result = result.detach().float()
    return result

# How the audio sample parameter is interpreted
def read_wave(audio_sample):
    _, audio_b64 = audio_sample.split('base64,')
    audio_bytes = base64.b64decode(audio_b64)
    audio_fl = io.BytesIO(audio_bytes)
    sr, pcm_data = read(audio_fl)
    assert sr == 16000
    assert pcm_data.ndim == 1
    return pcm_data

'''
# audio_sample comes from request
audio_sample = read_wave(audio_sample)
speech_auth(audio_sample)
'''
