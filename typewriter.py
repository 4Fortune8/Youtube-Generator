from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def create_typewriter_effect(text, output_dir, image_size=(1920, 1080), font_path='arial.ttf', font_size=24, line_height=30):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    lines = text.split('\n')
    max_lines = image_size[1] // line_height

    frame_number = 0
    current_text = []

    for p, line in enumerate(lines):
        for i in range(len(line) + 1):
            linepos=0
            current_text.append(line[:i])
            while len(current_text) > max_lines:
                current_text.pop(0)
            
            img = Image.new('RGB', image_size, color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_path, font_size)
            
            for j, text_line in enumerate(current_text):
                if text_line =="":
                    linepos+=1
                draw.text((1, linepos * line_height), text_line, font=font, fill=(255, 255, 255))
            
            img.save(os.path.join(output_dir, f'frame_{frame_number:04d}.png'))
            frame_number += 1
    subprocess.run(['ffmpeg', '-framerate', '30', '-i', os.path.join(output_dir, 'frame_%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(output_dir, 'typewriter_effect.mp4')])

# Usage example
text = """This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action."""

output_dir = 'typewriter_frames'
create_typewriter_effect(text, output_dir)
