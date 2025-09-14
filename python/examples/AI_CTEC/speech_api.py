from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import wave

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
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="RILOU7YmBhvwJGDGjNmP",
        model_id="eleven_v3",
        output_format="pcm_16000"
    )

    pcm_path = "ai_response_raw.pcm"
    wav_path = "ai_response_raw.wav"

    with open(pcm_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    pcm_to_wav(pcm_path, wav_path, channels=1, sample_rate=16000, sample_width=2)

    print("✅ Saved to ai_response_raw.wav")
    return wav_path
