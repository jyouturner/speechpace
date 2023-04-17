import numpy as np
import sounddevice as sd
import torch
import queue
from concurrent.futures import ThreadPoolExecutor
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize model and processor
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(device)
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

# Set up termination flag
terminate = False

# Set up audio buffer
audio_buffer = queue.Queue()

# Define audio_callback function
def audio_callback(indata, frames, time, status):
    audio_buffer.put(indata.copy())

# Define process_audio function with termination flag check
def process_audio():
    while not terminate:
        try:
            start_time = time.time()
            audio_data = audio_buffer.get(timeout=1)
            if audio_data is None:
                break
            audio_data = np.frombuffer(audio_data, dtype=np.int16)
            input_values = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_values.to(device)
            input_values = input_values.to(torch.float32)
            logits = model(input_values).logits
            pred_ids = torch.argmax(logits, dim=-1)
            transcript = processor.decode(pred_ids[0])
            # Calculate speaking pace
            words = len(transcript.split())
            duration = time.time() - start_time
            speaking_pace = words / duration
            print("Transcript:", transcript)
            print("Speaking pace: {:.2f} words per second".format(speaking_pace))
        except queue.Empty:
            pass

# Define Stream settings
stream = sd.InputStream(
    samplerate=16000, channels=1, dtype='int16', callback=audio_callback
)

# Start the ThreadPoolExecutor with the desired number of threads (e.g., 4)
with ThreadPoolExecutor(max_workers=4) as executor:
    with stream:
        print("Monitoring speaking pace... Press Ctrl+C to stop.")
        executor.submit(process_audio)
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print("Stopped monitoring.")
                break

# Set termination flag and wait for threads to exit
terminate = True
executor.shutdown(wait=True)
