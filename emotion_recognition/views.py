import librosa
import soundfile
import numpy as np
import pyaudio
import os
import wave
import pickle
from sys import byteorder
from array import array
from struct import pack
import glob
import os
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import AudioFileForm

# views.py

from django.contrib import messages

def emotion_recognition(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            if audio_file.name.split('.')[-1] != 'wav':
                messages.error(request, "Please upload a .wav file")
                return render(request, 'emotion_recognition/upload.html', {'form': form})
            with open("emotion_recognition_model\mlp_classifier.model", 'rb') as f:
                model = pickle.load(f);

            audio_file = request.FILES['audio_file']
            filename = "temp.wav"
            with open(filename, 'wb+') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
                
            features = extract_feature(filename, mfcc=True, chroma=True, mel=True).reshape(1, -1)
            predicted_emotion = model.predict(features)[0]

            return render(request, 'emotion_recognition/results.html', {'emotion': predicted_emotion})
    else:
        form = AudioFileForm()

    return render(request, 'emotion_recognition/upload.html', {'form': form})

"""
def extract_features(audio_data, sample_rate):
    # Extract Mel-frequency cepstral coefficients (MFCCs) from the audio data
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    mfccs_features = np.concatenate((mfccs_mean, mfccs_std))
    return mfccs_features
"""
def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
            result = np.hstack((result, tonnetz))
    return result 