import subprocess

def create_video_with_ffmpeg(image_path, audio_path, output_path, duration, text_overlay=None):
    # Create filter for text overlay if provided
    if text_overlay:
        text_filter = f"""drawtext=text='{text_overlay}'
        :fontcolor=green
        :fontsize=36
        :x=(w-text_w)/2
        :y=(h-text_h)/2
        :bordercolor=black
        :borderw=4
        """
    else:
        text_filter = ''

    # FFmpeg command to create a video from an image with an audio background and text overlay
    command = [
        'ffmpeg',
        '-loop', '1',                   # Loop the image
        '-i', image_path,               # Input image
        '-i', audio_path,               # Input audio
        '-c:v', 'libx264',              # Video codec
        '-t', str(duration),            # Duration of the video
        '-pix_fmt', 'yuv420p',          # Pixel format
        '-vf', f"scale=1920:1080,{text_filter}" if text_filter else 'scale=1920:1080', # Scale and optionally add text
        '-c:a', 'aac',                  # Audio codec
        '-b:a', '192k',                 # Audio bitrate
        '-shortest',                    # Finish encoding when the shortest input ends
        output_path                     # Output file
    ]

    # Run the FFmpeg command
    subprocess.run(command, check=True)

# Usage example

    
    
# Usage example
image_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\BackgroundCrop.jpg'
audio_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\from-beyond-royalty-free-no-copyright-background-music(1).wav'
output_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\output_video.mp4'
duration = 20  # Duration in seconds
text_overlay = "REEEE"

create_video_with_ffmpeg(image_path, audio_path, output_path, duration, text_overlay)
