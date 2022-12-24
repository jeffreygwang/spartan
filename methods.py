# General
import os
import openai
import requests # request img from web
import shutil # save img locally

# Audio Generation
import random
import string
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

# Speech To Text
from google.cloud import speech
import io

# Load Key
os.environ["OPENAI_API_KEY"] = "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"

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

class Images:
    def __init__(self, prompt, file_name):
        self.prompt = prompt
        self.file_name = file_name
    
    def generate(self):
        # Generate Image
        response = openai.Image.create(
            prompt=self.prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        print(f"Image URL: {image_url}")

        res = requests.get(image_url, stream = True)

        if res.status_code == 200:
            with open(self.file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', self.file_name)
        else:
            print('Image Couldn\'t be retrieved')

class SpeechToText:
    def __init__(self, file: str):
        self.file = file
        self.encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
        self.sample_rate = 16000
        self.language_code = "en-US"
        self.transcript = ""

    def speechtotext(self):
        client = speech.SpeechClient()

        with io.open(self.file, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=self.encoding,
            sample_rate_hertz=self.sample_rate,
            language_code=self.language_code,
        )

        response = client.recognize(config=config, audio=audio)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.

        complete_transcript = ""
        for result in response.results:
            complete_transcript += result.alternatives[0].transcript
        
        self.transcript = complete_transcript
        return complete_transcript

class AudioGeneration:

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def __init__(self, name: str):
        self.name = name
        self.samplerate = 16000
        self.subtype = "PCM_16"
        self.channels = 1
        self.device = 1
        self.filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + ".wav"
        self.q = queue.Queue()
    
    def record(self):
        try:
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                            channels=self.channels, subtype=self.subtype) as file:
                with sd.InputStream(samplerate=self.samplerate, channels=self.channels, 
                            callback=self.callback):
                    print('#' * 80)
                    print('press Ctrl+C to stop the recording')
                    print('#' * 80)
                    while True:
                        file.write(self.q.get())

        except KeyboardInterrupt:
            print('\nRecording finished: ' + repr(self.filename))


