import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found — check your .env file")

# Create Groq client
client = Groq(api_key=api_key)

SYSTEM_PROMPT = """You are a helpful, harmless, and honest personal assistant.
Answer questions clearly and concisely.
If you don't know something, say so honestly — never make up facts.
Avoid harmful, biased, or dangerous content."""

print("Groq client ready.")


def generate_response(messages: list) -> str:
    """
    Takes messages in our standard format.
    Sends to Groq API and returns response.
    """

    # Build formatted messages
    formatted_messages = []

    # Add system prompt first
    formatted_messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })

    # Add conversation history + current message
    for msg in messages:
        if msg["role"] == "system":
            continue  # already added above
        formatted_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=formatted_messages,
        max_tokens=512,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()