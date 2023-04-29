import librosa
import soundfile as sf


def change_playback_speed(input_file, output_file, speed_factor):
    y, sr = librosa.load(input_file, sr=None)
    y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    sf.write(output_file, y_fast, sr)
    print("Created", output_file)
    return output_file

if __name__ == "__main__":
    change_playback_speed("recording.m4a", "recording_3.00.wav", 3.00)