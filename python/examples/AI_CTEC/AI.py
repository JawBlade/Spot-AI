#!/usr/bin/env python3

import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI

from speech_api import elevenlabs_api
from helpers import adjust_volume
from search_agent import fetch_live_info
from helpers import load_on_spot, play_on_spot, delete_from_spot, record
from memory import init_db, add_conversation, get_last_conversations

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

path = DB_PATH = "/home/jaw_blade/my_spot_env/spot-sdk/python/examples/AI_CTEC/spot_memory.db"
init_db(path)

AUDIO_FILE = Path("h264.sdp.wav")
TTS_RAW_FILE = Path("ai_response_raw.wav")
FINAL_WAV_FILE = Path("ai_response.wav")

SYSTEM_PROMPT = (
    "MOST IMPORTANT RULE: If the user’s question requires current, recent, or time-sensitive information "
    "(e.g., “What day is it?”, “Latest news on…”, “Current firmware version”), do not answer from your pre-trained knowledge. "
    "Instead, reply exactly: “I do not have information on that.” Only answer from your own knowledge if the question is not time-sensitive or recent. "
    "You will provide tags in brackets to indicate tone and emotion because this will be used with elevenlabs api. "
    "You are a friendly assistant in the CTEC robotics lab called Bumblebee. "
    "Answer questions with tags about NAO, Pepper, PLCs, Universal Robots, KUKAs, and MiRs as if talking to a student. "
    "Keep answers very short, conversational and casual, about a 10sec response or less. Explain simply unless the student specifically asked for a longer response."
)

# -------------------- HELPER FUNCTIONS --------------------
async def transcribe_audio(file_path: Path) -> str:
    """Transcribes audio using OpenAI Whisper API."""
    with open(file_path, "rb") as f:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcription.text

async def get_gpt_response(user_text: str) -> str:
    """Gets a response from GPT-5-Nano."""
    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

def generate_final_wav(text: str, raw_path: Path, final_path: Path, volume: float = 1.0) -> None:
    """Generate TTS WAV file and adjust volume."""
    raw_file = elevenlabs_api(text)
    adjust_volume(raw_file, final_path, volume)
    return final_path

async def main():
    print("Recording audio...")
    # record()

    try:
        transcription_text = await transcribe_audio(AUDIO_FILE)
    except Exception as e:
        print("Error transcribing audio:", e)
        return

    print("Transcribed text:", transcription_text)

    try:
        text_to_speak = await get_gpt_response(transcription_text)
    except Exception as e:
        print("Error getting GPT response:", e)
        return

    # Check if GPT cannot answer and fallback to live agent
    if "i do not have information on that" in text_to_speak.lower():
        try:
            text_to_speak = await fetch_live_info(transcription_text)
        except Exception as e:
            print("Error fetching live info:", e)
            return

    add_conversation(transcription_text, text_to_speak, path)
    print("Final text to speak:", text_to_speak)

    try:
        generate_final_wav(text_to_speak, TTS_RAW_FILE, FINAL_WAV_FILE)
    except Exception as e:
        print("Error generating WAV file:", e)
        return

    print(f"Final WAV file ready: {FINAL_WAV_FILE}")

    # load_on_spot()
    # play_on_spot()
    # delete_from_spot()

if __name__ == "__main__":
    asyncio.run(main())
