import requests
import base64
import os

# Text to generate audio for
TEXT = "(I'm a scary voice!)"

# Get the API key from the environment variable
KEY = os.getenv('INWORLD_API_KEY')
KEY = 'NmowRmNFUkQwQ2VWWDI4SmlGTzg4blQ4NFJVSWY3dmg6d1kycjdmRnJUUlppN1F5d1MyaXhsYVE2NTRFZlUxWklsTHpkZzgxQ3VrdGpCOWx4ZmNLRUg5bzNmSWNSaXR1Rg=='
url = "https://api.inworld.ai/tts/v1/voice"
headers = { "Authorization": f"Basic {KEY}", "Content-Type": "application/json" }

def create_audio(text: str, output_file: str = "audio.mp3") -> str:
    """Convert *text* to speech (MP3) via Inworld TTS and return the saved path."""
    payload = {
        "text": text,
        "voiceId": "Hades",
        "modelId": "inworld-tts-1",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    audio_content = base64.b64decode(result["audioContent"])

    with open(output_file, "wb") as f:
        f.write(audio_content)

    return os.path.abspath(output_file)


# ---------------------------------------------------------------------------
# CLI / debug usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # If run directly, generate audio from the default TEXT constant
    output_path = create_audio(TEXT)
    print(f"Audio saved to {output_path}")
