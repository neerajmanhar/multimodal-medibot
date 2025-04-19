# from dotenv import load_dotenv
import base64
import os
from groq import Groq
# load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").replace("\n", "").replace("\r", "").strip()
headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}


query="Is there something wrong with my face?"
model="llama-3.2-90b-vision-preview"

def encode_image(image_path):   
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image_with_query(query, model, encoded_image):
    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content

def analyze_without_image(query, model):
    client = Groq()
    chat_completion = client.chat.completions.create(
        
        messages=[
            {
                "role": "system",
                "content": "you are a helpful medical professional."
            },
            {
                "role": "user",
                "content": query,
            }
        ],

        model=model
    )
    
    return chat_completion.choices[0].message.content