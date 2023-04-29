import numpy as np
import pyaudio
import wave
import os
import librosa
import joblib
import sys

def extract_features(file_name):
    audio, sample_rate = librosa.load(file_name, sr=None, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    mfccs_std = np.std(mfccs.T, axis=0)

    return np.hstack([mfccs_mean, mfccs_std])


def record_audio(output_file, seconds):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()




def predict(audio_file):
    # Extract features from the recorded audio
    audio_features = extract_features(audio_file)
    print(audio_features)
    # Use the SVM model to predict whether the audio is too fast
    prediction = clf.predict([audio_features])  # No need to remove the label from the features

    # Remove the temporary audio file
    os.remove(audio_file)

    # Interpret the prediction result
    if prediction[0] == 1:
        print("The audio is not fast.")
    else:
        print("The audio is too fast.")

# print("Usage: python train_model.py <path_to_audio_file>")
if __name__ == "__main__":
    # Load the trained SVM model
    clf = joblib.load('trained_svm_model.joblib')
    if len(sys.argv) == 2:
        
        audio_file = sys.argv[1]
    else:
        # Record audio from the microphone
        audio_file = "temp_recording.wav"
        record_audio(audio_file, 5)
    predict(audio_file)
