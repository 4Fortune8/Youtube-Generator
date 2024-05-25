from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def create_typewriter_effect(text, output_dir, image_size=(1920, 1080), font_path='arial.ttf', font_size=24, line_height=30):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    lines = text.split('\n')
    max_lines = 25
    Ystartpix = 800
    Xstartpix = 190
    frame_number = 0
    current_text = []
    old_text = []
    mostrecentpos=0
    skiptolines=0
    for p, line in enumerate(lines):
        img = Image.new('RGB', image_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        for i in range(skiptolines, p):
            if i == skiptolines:
                img = Image.new('RGB', image_size, color=(0, 0, 0))
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(font_path, font_size)
            draw.text((Xstartpix, Ystartpix+((i-p-1) * line_height)), lines[i], font=font, fill=(255, 255, 255))
            
        if p > max_lines:
                    skiptolines+=1
        if p == mostrecentpos:
            current_text= []
            for i in range(len(line) + 1):
                current_text.append(line[:i])
                
                for j, text_line in enumerate(current_text):
                    if text_line =="" :
                        old_text.append(text_line)
                        
                    else:                    
                        draw.text((Xstartpix, Ystartpix+((skiptolines) * line_height)), text_line, font=font, fill=(255, 255, 255))
                img.save(os.path.join(output_dir, f'frame_{frame_number:04d}.png'))
                frame_number += 1
                
        
        mostrecentpos += 1
    subprocess.run(['ffmpeg', '-framerate', '30', '-i', os.path.join(output_dir, 'frame_%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(output_dir, 'typewriter_effect.mp4')])

# Usage example
text = """This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action.
This is a line of text.
This is another line of text.
This is yet another line of text.
Typewriter effect in action."""

output_dir = 'typewriter_frames'
create_typewriter_effect(text, output_dir)
