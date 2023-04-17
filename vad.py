import numpy as np
import sounddevice as sd
import time
import webrtcvad
import threading

SAMPLE_RATE = 16000
BLOCK_SIZE = 480
WINDOW_SIZE = 10

vad = webrtcvad.Vad(3)
speech_frames = []

def calculate_speaking_pace(speech_frames, window_size):
    speech_frame_count = len(speech_frames)
    speaking_pace = speech_frame_count / window_size
    return speaking_pace

def audio_processing(indata):
    global speech_frames
    audio_data = np.frombuffer(indata, dtype=np.int16)
    frame_count = len(audio_data) // BLOCK_SIZE

    for i in range(frame_count):
        frame = audio_data[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        is_speech = vad.is_speech(frame.tobytes(), SAMPLE_RATE)

        if is_speech:
            speech_frames.append(frame)

        if len(speech_frames) > WINDOW_SIZE * SAMPLE_RATE // BLOCK_SIZE:
            speech_frames.pop(0)

    speaking_pace = calculate_speaking_pace(speech_frames, WINDOW_SIZE)
    print(f"Speaking pace: {speaking_pace:.2f} speech frames ratio")

    silence = True
    for frame in speech_frames:
        if vad.is_speech(frame.tobytes(), SAMPLE_RATE):
            silence = False
            break

    if silence:
        speech_frames = []

def audio_callback(indata, frames, time, status):
    audio_thread = threading.Thread(target=audio_processing, args=(indata,))
    audio_thread.start()

with sd.InputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, channels=1, dtype=np.int16, callback=audio_callback):
    print("Monitoring speaking pace... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
