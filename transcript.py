from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import numpy as np
import soundfile as sf

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(device)

def transcribe_file(file_path):
    audio, _ = sf.read(file_path)
    audio = (audio * 32768).astype(np.int16)
    input_values = processor(audio, return_tensors="pt", padding=True, sampling_rate=16000).input_values.to(device)
    input_values = input_values.to(torch.float32)
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcript = processor.decode(predicted_ids[0])
    return transcript

transcript = transcribe_file("test_recording.wav")
print("Transcript:", transcript)
