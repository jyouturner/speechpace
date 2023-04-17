import numpy as np
import sounddevice as sd
import time
import webrtcvad
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

BLOCK_SIZE = 480
WINDOW_SIZE = 10
SAMPLE_RATE = 16000

# Create a VAD object.
vad = webrtcvad.Vad(3)
speech_frames = []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.last_speech_time = 0
        self.label = QLabel()
        self.button = QPushButton("Start")

        self.button.clicked.connect(self.start_monitoring)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def start_monitoring(self):


        # Create a thread to monitor the audio input.
        audio_thread = threading.Thread(target=self.audio_processing)
        audio_thread.start()

        # Start the GUI event loop.
        app.exec_()

    def audio_processing(self):
        # Open the audio stream.
        with sd.InputStream(samplerate=16000, blocksize=480, channels=1, dtype=np.int16, callback=self.audio_callback):
            print("Monitoring speaking pace... Press Ctrl+C to stop.")

            # Keep the program running until the user presses Ctrl+C.
            while True:
                time.sleep(1)

    def audio_callback(self, indata, frames, time, status):
        global speech_frames
        audio_data = np.frombuffer(indata, dtype=np.int16)
        frame_count = len(audio_data) // BLOCK_SIZE

        for i in range(frame_count):
            frame = audio_data[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
            is_speech = vad.is_speech(frame.tobytes(), SAMPLE_RATE)

            if is_speech:
                speech_frames.append(frame)

            if len(speech_frames) > 10 * 16000 // 480:
                speech_frames.pop(0)

            speaking_pace = calculate_speaking_pace(speech_frames, 10)
            if not is_speech or time - self.last_speech_time > 0.5:
                self.label.setText("")
        self.label.setText(f"Speaking pace: {speaking_pace:.2f} speech frames ratio")
        self.last_speech_time = time


def calculate_speaking_pace(speech_frames, window_size):
    speech_frame_count = len(speech_frames)
    speaking_pace = speech_frame_count / window_size
    return speaking_pace


if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec_()
