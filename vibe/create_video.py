
# Gotta install old version because new version of moviepy does NOT have editor!!!
# pip uninstall moviepy -y
# pip install moviepy==1.0.3

import os
from moviepy.editor import AudioFileClip, ImageClip

def validate_files(audio_path: str, image_path: str) -> bool:
    """
    Validate that the input files exist and are the correct format.
    """
    if not os.path.exists(audio_path):
        print(f"Error: Audio file '{audio_path}' does not exist")
        return False
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' does not exist")
        return False
    
    # Check file extensions
    if not audio_path.lower().endswith('.mp3'):
        print("Error: Audio file must be an MP3")
        return False
    
    if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        print("Error: Image file must be JPG or PNG")
        return False
    
    return True

def create_video(audio_path: str, image_path: str, output_path: str) -> None:
    """
    Create a video from a static image and an audio file.
    """
    try:
        # Load the audio file
        print("Loading audio file...")
        audio = AudioFileClip(audio_path)
        print(f"Audio duration: {audio.duration} seconds")
        print(f"Audio fps: {audio.fps}")
        
        # Load the image file
        print("Loading image file...")
        image = ImageClip(image_path)
        
        # Set the duration of the image to match the audio
        video = image.set_duration(audio.duration)
        
        # Set the audio
        video = video.set_audio(audio)
        
        # Write the video file
        print(f"Creating video file at {output_path}...")
        print(f"Video duration: {video.duration} seconds")
        print(f"Video has audio: {video.audio is not None}")
        if video.audio:
            print(f"Video audio duration: {video.audio.duration} seconds")
        video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        print("Video creation completed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up
        if 'audio' in locals():
            audio.close()
        if 'video' in locals():
            video.close()

def main():
    audio_file = 'audio.mp3'
    image_file = 'image.jpg'
    output_file = 'video.mp4'
    
    if validate_files(audio_file, image_file):
        create_video(audio_file, image_file, output_file)

if __name__ == '__main__':
    main()