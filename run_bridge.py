import os
import asyncio
from dotenv import load_file  # Assuming usage of a basic env loader or exporting via bash
from 3_ai_services.gemini_bridge.main import process_voice_command

async def test_pipeline():
    # Simulate a voice command captured by the Spectrum-Z0ne microphones
    sample_command = "Check my crypto alerts and turn on sun shade mode"
    print(f"Sending to Gemini: '{sample_command}'...")
    
    response = await process_voice_command(sample_command)
    print(f"Dashboard Response: {response}")

if __name__ == "__main__":
    # Ensure GEMINI_API_KEY is present in environment
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
    else:
        asyncio.run(test_pipeline())
