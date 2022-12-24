import os
import openai
import glob
import methods

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load Key
os.environ["OPENAI_API_KEY"] = "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"

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

# wav Cleanup
for file in glob.glob("*.wav"):
    os.remove(file)

for file in glob.glob("*.png"):
    os.remove(file)

# Grab Speech
speech_obj = methods.AudioGeneration("audiogenerate")
speech_obj.record()

# Translate to Text
text_trans = methods.SpeechToText(speech_obj.filename)
transcript: str = text_trans.speechtotext()
print(f"Transcript: {transcript}")

# Generate Image
imagegen = methods.Images(transcript, "temp.png")
imagegen.generate()
img = mpimg.imread('temp.png')
imgplot = plt.imshow(img)
plt.show()



