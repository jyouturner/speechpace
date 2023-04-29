import numpy as np
import pyaudio
import os
import librosa
import joblib

def extract_features(audio_data, sample_rate):
    audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32767.0
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13, n_fft=1024)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    mfccs_std = np.std(mfccs.T, axis=0)

    return np.hstack([mfccs_mean, mfccs_std])


def predict(audio_data, sample_rate):
    audio_features = extract_features(audio_data, sample_rate)
    prediction = clf.predict([audio_features])

    if prediction[0] == 1:
        # print("The audio is not fast.")
        pass
    else:
        print("The audio is too fast.")

def callback(in_data, frame_count, time_info, status):
    predict(in_data, sample_rate)
    return (in_data, pyaudio.paContinue)

sample_rate = 44100
clf = joblib.load('trained_svm_model.joblib')

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=1024,
                stream_callback=callback)

try:
    print("Start listening...")
    stream.start_stream()
    while stream.is_active():
        # Run the loop while the stream is active
        pass
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    # Properly close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
