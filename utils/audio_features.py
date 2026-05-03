import librosa
import numpy as np

def extract_features(file_path):
    signal, sample_rate = librosa.load(file_path, sr=None)

    mfccs = np.mean(
        librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40),
        axis=1
    )

    chroma = np.mean(
        librosa.feature.chroma_stft(y=signal, sr=sample_rate),
        axis=1
    )

    mel = np.mean(
        librosa.feature.melspectrogram(y=signal, sr=sample_rate),
        axis=1
    )

    return np.concatenate([mfccs, chroma, mel])
