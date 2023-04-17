import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

rec_duration = 5  # Record for 5 seconds
rec_fs = 16000

recording = sd.rec(int(rec_duration * rec_fs), samplerate=rec_fs, channels=1)
sd.wait()

wav.write("test_recording.wav", rec_fs, recording)
