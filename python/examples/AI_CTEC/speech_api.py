from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import logging
import os
import wave

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def pcm_to_wav(pcm_file, wav_file, channels=1, sample_rate=16000, sample_width=2):
    with open(pcm_file, 'rb') as pcm_f:
        pcm_data = pcm_f.read()
    with wave.open(wav_file, 'wb') as wav_f:
        wav_f.setnchannels(channels)
        wav_f.setsampwidth(sample_width)
        wav_f.setframerate(sample_rate)
        wav_f.writeframes(pcm_data)

def elevenlabs_api(text: str):
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="MFZUKuGQUsGJPQjTS4wC",
            model_id="eleven_v3",
            output_format="pcm_16000"
        )
        pcm_path = "ai_response_raw.pcm"
        wav_path = "ai_response_raw.wav"

        with open(pcm_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        pcm_to_wav(pcm_path, wav_path, channels=1, sample_rate=16000, sample_width=2)

        logger.info(f"Saved ElevenLabs PCM audio to {pcm_path}")
        logger.info(f"✅ Saved to {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error generating TTS audio: {e}")
        return None
