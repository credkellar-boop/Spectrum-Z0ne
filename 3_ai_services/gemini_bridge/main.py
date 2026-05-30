import os
import asyncio
from google import genai

async def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set.")
        return

    client = genai.Client(api_key=api_key)
    print("Gemini AI Bridge Active. Awaiting WebRTC stream data...")

    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Gemini AI Bridge Offline.")
            break

if __name__ == "__main__":
    asyncio.run(main())
