import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import coremltools as ct
import sys
import librosa
import numpy as np
import os
import joblib

def change_playback_speed(input_file, speed_factor):
    y, sr = librosa.load(input_file, sr=None)
    y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    return y_fast, sr

def extract_features(audio, sample_rate, class_label):
    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)

    # Calculate the mean and standard deviation for each MFCC feature
    mfccs_mean = np.mean(mfccs.T, axis=0)
    mfccs_std = np.std(mfccs.T, axis=0)

    # Combine the mean and standard deviation values and append the class label
    return np.hstack([mfccs_mean, mfccs_std, int(class_label)]).astype(np.int32)

def train_model(file_path):
    # Define playback speeds and corresponding class labels
    playback_speeds = [0.50, 0.70, 0.80, 0.90, 1.00, 1.04, 1.06, 1.08, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80]
    class_labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]

    # Extract features from the audio file
    all_features = []
    for speed, label in zip(playback_speeds, class_labels):
        audio, sample_rate = change_playback_speed(file_path, speed)
        all_features.append(extract_features(audio, sample_rate, label))

    all_features = np.array(all_features)
    print("Extracted features from", len(all_features), "audio files")
   
    all_features = np.vstack(all_features)
    
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(all_features[:, :-1], all_features[:, -1], test_size=0.25, random_state=42)

    # Train the SVM model
    clf = SVC(kernel='linear', C=1, probability=True, random_state=42)
    clf.fit(X_train, y_train)
    print("Trained SVM model", clf)
    print(X_train.shape, y_train.shape)
    joblib.dump(clf, 'trained_svm_model.joblib')

    # Convert the trained SVM model to Core ML format
    coreml_model = ct.converters.sklearn.convert(clf)

    # Save the Core ML model
    coreml_model.save("TrainedModel.mlmodel")

    # Print the model accuracy
    accuracy = clf.score(X_test, y_test)
    print("Model accuracy: {:.2f}%".format(accuracy * 100))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python train_model.py <path_to_audio_file>")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    train_model(audio_file_path)
