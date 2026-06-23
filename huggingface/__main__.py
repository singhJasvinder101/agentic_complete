from transformers import pipeline

pipe = pipeline("image-text-to-text", model="google/t5gemma-2-1b-1b")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://img.magnific.com/free-photo/beautiful-scenery-emerald-lake-yoho-national-park-british-columbia-canada_181624-6877.jpg"
            },
            {
                "type": "text",
                "text": "What is in the image?"
            }
        ]
    }
]

if __name__ == "__main__":
    response = pipe(messages)
    