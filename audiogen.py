import random
import string

import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class audiogenerate:

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


