from google.cloud import speech
import os
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jeffreywang/.config/gcloud/application_default_credentials.json"

class speechrecognition:
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



