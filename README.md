# Realtime Speech Pace Monitor

Do you feel sometimes you talk too fast? This is (hopefully) useful for you to monitor your talking pace.

## How It Works

This Python project will get audio from microphone and figure out your speech pace while you are talking.

Some considerations in the design:

1. we can not rely on external API due to the concern of performance and privacy. That eliminates the ChatGPT Wisper etc.
2. Although there are multiple packages to do text-to-speech, then voice-to-text might not be the most efficient approach. 
3. We can estimate the speaking pace by analyzing the audio signal directly.

The choosen solution is to use existing VAD library like webrtcvad to achieve this.

````
With help from ChatGPT and Google Bard, 

vad.py: the working version of python code to monitor pace when you are speaking
record.py: the testing code to record voice to local file
transcript.py: the testing code to transcript the local recorded file
bard.py: the code from Google Bard

````

## Run It

````sh
python3 vad.py
````

## To Update

Setup Local Dev

````sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````