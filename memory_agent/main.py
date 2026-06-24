from warnings import filters
import json
import os

from openai import OpenAI
from mem0 import Memory


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key") 
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
MEMORY_MODEL = os.getenv("OPENAI_MEMORY_MODEL", CHAT_MODEL)

client = OpenAI(api_key=OPENAI_API_KEY)

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": MEMORY_MODEL,
            "api_key": OPENAI_API_KEY
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": OPENAI_API_KEY
        }
    }
}

mem_client: Memory = Memory.from_config(config)

while True:
    query = input("> ")

    old_memories = mem_client.search(query, filters={'user_id': 'user_1'}, limit=3)

    memories = [f"ID: {m.get('id')}, Memory: {m.get('memory')}" for m in old_memories.get('results', [])]


    SYSTEM_PROMPT = f"""
    Here is about the context about the user:
    {json.dumps(memories, indent=2)}
    """

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user", 
                "content": query
            }
        ]
    )


    mem_client.add(
        user_id="user_1",
        messages=[
            {
                "role": "user",
                "content": query
            },
            {
                "role": "assistant",
                "content": response.choices[0].message.content
            }
        ]
    )

    print("Memory saving.... Response:", response.choices[0].message.content)