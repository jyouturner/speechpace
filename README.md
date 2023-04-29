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

## Speech Pace Monitoring on iPhone

Our approach for integrating your iOS app with a Python API to train a model using the recorded audio files. Here's an overview of the design:

    iOS app requests a pre-signed S3 URL and UUID from the Python API.
    iOS app uploads the recorded audio file directly to S3.
    iOS app polls the Python API to check if the model is ready.
    Python API is implemented using AWS API Gateway and AWS Lambda.
    Another Lambda function is triggered by an S3 event when a new audio file is uploaded, which trains the model and saves it to S3.

This design is efficient because it offloads the model training process to AWS Lambda and stores the intermediate files (audio and trained models) on S3. The use of pre-signed URLs allows for secure and direct communication between the iOS app and S3, without the need to route the file transfer through your server.

Moreover, this design scales well, as AWS Lambda can process multiple files concurrently and independently, allowing you to handle many requests simultaneously.



`Note: librosa does not work for Python 3.11.2, thus we have to use Python3.10`

````sh
pip install virtualenv
virtualenv -p python3.10 venv310
source venv310/bin/activate
pip install -r requirements.txt
brew install ffmpeg
````

Note `ffmpeg is used to save m4a file`