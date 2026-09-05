"""
Shared feature extraction for EmoSense AI.

IMPORTANT: This exact file is used both to build the training set
(training/preprocessing.py) and at inference time (services/emotion_service.py).
If you change anything here, you MUST regenerate features.npy/labels.npy
and retrain — a mismatch between train-time and inference-time features
is the #1 cause of a model that scores well offline but performs badly
in production.

Feature set (up from 220 -> ~193 richer, more temporally-aware dims):
  - MFCC (40) mean + MFCC delta (40) mean + MFCC delta-delta (40) mean
  - Chroma STFT (12) mean
  - Mel spectrogram (128) mean  -> reduced via log + mean, same as before
  - Spectral contrast (7) mean
  - Zero-crossing rate (1) mean
  - RMS energy (1) mean

Delta/delta-delta MFCCs capture HOW sound changes over time (pitch/energy
trajectory), which is a lot of what carries emotion — plain MFCC means
throw that away.
"""
import librosa
import numpy as np


def extract_features(file_path, augment=None):
    """
    Extract a fixed-length feature vector from an audio file.

    augment: None, or one of "noise", "pitch", "stretch" — used only
    during training to synthetically expand the dataset. Never used
    at inference time.
    """
    signal, sample_rate = librosa.load(file_path, sr=None)

    if augment == "noise":
        noise_amp = 0.005 * np.random.uniform() * np.amax(signal)
        signal = signal + noise_amp * np.random.normal(size=signal.shape[0])
    elif augment == "pitch":
        n_steps = np.random.uniform(-2, 2)
        signal = librosa.effects.pitch_shift(signal, sr=sample_rate, n_steps=n_steps)
    elif augment == "stretch":
        rate = np.random.uniform(0.85, 1.15)
        signal = librosa.effects.time_stretch(signal, rate=rate)

    mfcc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    chroma = librosa.feature.chroma_stft(y=signal, sr=sample_rate)
    mel = librosa.feature.melspectrogram(y=signal, sr=sample_rate)
    mel_db = librosa.power_to_db(mel)  # log-scale, much more informative than raw power

    contrast = librosa.feature.spectral_contrast(y=signal, sr=sample_rate)
    zcr = librosa.feature.zero_crossing_rate(y=signal)
    rms = librosa.feature.rms(y=signal)

    features = np.concatenate([
        np.mean(mfcc, axis=1),
        np.mean(mfcc_delta, axis=1),
        np.mean(mfcc_delta2, axis=1),
        np.mean(chroma, axis=1),
        np.mean(mel_db, axis=1),
        np.mean(contrast, axis=1),
        np.mean(zcr, axis=1),
        np.mean(rms, axis=1),
    ])

    return features