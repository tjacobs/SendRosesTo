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

# Generate the audio
payload = {
    "text": TEXT,
    "voiceId": "Hades",
    "modelId": "inworld-tts-1"
}
response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()
result = response.json()
audio_content = base64.b64decode(result['audioContent'])

# Save the audio to a file
with open("audio.mp3", "wb") as f:
    f.write(audio_content)
