import numpy as np
import sounddevice as sd
import webrtcvad
import time

sample_rate = 16000
window_duration = 0.03
vad_mode = 3
threshold = 32.0

frame_len = int(sample_rate * window_duration)
buffer_len = 50

vad = webrtcvad.Vad()
vad.set_mode(vad_mode)

buffer = []

def audio_callback(indata, callback_frames, time, status):
    audio_data = indata[:, 0]
    audio_data_pcm = (audio_data * 32768).astype(np.int16)

    num_frames = len(audio_data_pcm) // frame_len
    if num_frames > 0:
        new_frames = np.array_split(audio_data_pcm, num_frames)

        for frame in new_frames:
            is_speech = vad.is_speech(frame.tobytes(), sample_rate)
            buffer.append(is_speech)

            if len(buffer) > buffer_len:
                buffer.pop(0)

        speaking_pace = sum(buffer) / (buffer_len * window_duration)
        # print("Speaking pace:", speaking_pace, "speech segments per second")

        if speaking_pace > threshold:
            print("You're speaking too fast!", speaking_pace, ">", threshold)

with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback, blocksize=frame_len):
    print("Monitoring speaking pace... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped monitoring.")
