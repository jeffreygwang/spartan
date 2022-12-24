import os
import openai
import requests # request img from web
import shutil # save img locally

# Load Key
os.environ["OPENAI_API_KEY"] = "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"

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

class imager:
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
