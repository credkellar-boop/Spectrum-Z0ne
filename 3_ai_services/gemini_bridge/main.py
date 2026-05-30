import os
import asyncio
import io
import PIL.Image
from google import genai
from google.genai import types

# Initialize the async client for low-latency non-blocking calls
client = genai.Client().aio

async def process_voice_command(user_audio_text: str):
    """Handles standard voice inputs for the Spectrum-Z0ne dashboard."""
    response = await client.models.generate_content(
        model='gemini-3.5-flash',
        contents=f"User Command: {user_audio_text}\nDetermine the action for the AR dashboard.",
        config=types.GenerateContentConfig(
            temperature=0.2,
            system_instruction="You are the intelligence layer for Spectrum-Z0ne AR glasses. Keep responses under 10 words."
        )
    )
    return response.text

async def analyze_visual_hub(image_bytes: bytes, prompt: str):
    """Processes 4K camera frames for real-time contextual awareness."""
    image = PIL.Image.open(io.BytesIO(image_bytes))
    
    response = await client.models.generate_content(
        model='gemini-3.5-flash',
        contents=[prompt, image],
    )
    return response.text
