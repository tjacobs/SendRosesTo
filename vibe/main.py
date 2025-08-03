"""High-level script to:
1. Generate a poem using OpenAI
2. Convert the poem to speech using Inworld TTS
3. Combine the audio with a static image to produce a video

Prerequisites:
- OPENAI_API_KEY environment variable (or configured in create_poem.py)
- INWORLD_API_KEY environment variable (or fallback key in create_audio.py)
- image.jpg in the same directory (or modify IMAGE_FILE below)
"""

from pathlib import Path

from create_poem  import create_poem
from create_audio import create_audio
from create_video import create_video

POEM_FILE  = Path("poem.txt")
AUDIO_FILE = Path("audio.mp3")
IMAGE_FILE = Path("image.jpg")
VIDEO_FILE = Path("video.mp4")

def main() -> None:
    # 1. Generate poem
    poem = create_poem(PROMPT)
    print("\nGenerated Poem:\n---------------\n" + poem)
    POEM_FILE.write_text(poem, encoding="utf-8")
    print(f"Poem saved to {POEM_FILE}")

    # 2. Generate audio from poem
    audio_path = create_audio(poem, str(AUDIO_FILE))
    print(f"Audio saved to {audio_path}")

    # 3. Create video combining image and audio
    if not IMAGE_FILE.exists(): raise FileNotFoundError(f"Image file '{IMAGE_FILE}' not found. Please provide an image.")
    create_video(str(AUDIO_FILE), str(IMAGE_FILE), str(VIDEO_FILE))
    print(f"Video saved to {VIDEO_FILE}")

if __name__ == "__main__":
    main()