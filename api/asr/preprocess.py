"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
import librosa
import numpy as np
import glob
import os

def preprocess_audio(file_path, sample_rate=16000, n_mels=80):
    """
    Loads an audio file, resamples, normalizes, and extracts Mel Spectrogram features.
    Args:
        file_path (str): Path to the audio file.
        sample_rate (int): Target sample rate.
        n_mels (int): Number of Mel filterbanks.
    Returns:
        np.ndarray: Mel Spectrogram features.
    """
    # Load audio
    waveform, sr = librosa.load(file_path, sr=sample_rate, mono=True)
    # Normalize
    waveform = waveform / np.max(np.abs(waveform))
    # Mel Spectrogram
    mel_spec = librosa.feature.melspectrogram(y=waveform, sr=sample_rate, n_mels=n_mels)
    # Convert to log scale
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
    return log_mel_spec

def preprocess_files(file_list, sample_rate=16000, n_mels=80, save_dir=None):
    """
    Processes a list of audio files and returns their features.
    Optionally saves each feature array as a .npy file in save_dir.
    Args:
        file_list (list): List of audio file paths.
        sample_rate (int): Target sample rate.
        n_mels (int): Number of Mel filterbanks.
        save_dir (str or None): Directory to save .npy features. If None, does not save.
    Returns:
        dict: {file_path: features}
    """
    features_dict = {}
    for file_path in file_list:
        features = preprocess_audio(file_path, sample_rate, n_mels)
        features_dict[file_path] = features
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            base = os.path.splitext(os.path.basename(file_path))[0]
            np.save(os.path.join(save_dir, base + '.npy'), features)
    return features_dict

# Ses dosyalarının bulunduğu klasör
AUDIO_DIR = "../data/mmmdeng"
# Özelliklerin kaydedileceği klasör
FEATURES_DIR = "../data/mmmfeatures"

# Tüm .wav dosyalarını bul
audio_files = glob.glob(os.path.join(AUDIO_DIR, "*.wav"))

# Özellikleri çıkar ve kaydet
features = preprocess_files(audio_files, sample_rate=16000, n_mels=80, save_dir=FEATURES_DIR)

print(f"{len(features)} dosya işlendi ve özellikler {FEATURES_DIR} klasörüne kaydedildi.")
