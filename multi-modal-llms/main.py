from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user", 
            "content": [
                { "type": "text", "text": "what you can see in the image?" },
                { "type": "image_url", "image_url": { "url": "https://images.unsplash.com/photo-1773332585698-cba3c91b73e4?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" } }
            ]
        }
    ]
)
        

print(response.choices[0].message.content)
