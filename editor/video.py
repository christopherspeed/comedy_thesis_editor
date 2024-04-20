"""
Utilities module covering the video editing functionalities used by the central
editor model.
"""

import numpy as np
import subprocess
import tempfile
import os
import uuid

def assemble(clips: "list[dict]", output_video_filename="Output_Video.mp4") -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
                
        temp_clips = []
        for clip in clips:
            clip_filename = clip["filename"]
            start, end = clip["start"], clip["end"]
            # remove ending filename, make ensure that we can take multiple sections of the same clip
            temp_clip = os.path.join(temp_dir, f'{clip_filename[:-4]}_{str(uuid.uuid4())}.mp4')
            print("Temporary clip name", temp_clip)
            
            if end == -1: # final clip
                extract_command = [
                    'ffmpeg', 
                    '-y', 
                    '-i', 
                    clip_filename, 
                    '-ss', 
                    str(start), 
                    # Add re-encoding options
                    '-c:v', 'libx264',  # Video codec
                    '-c:a', 'aac',      # Audio codec
                    '-preset', 'fast',  # Encoding preset
                    temp_clip
                ]
            else:
                extract_command = [
                    'ffmpeg', 
                    '-y', 
                    '-i', 
                    clip_filename, 
                    '-ss', 
                    str(start), 
                    '-t', 
                    str(end - start), 
                    # Add re-encoding options
                    '-c:v', 'libx264',  # Video codec
                    '-c:a', 'aac',      # Audio codec
                    '-preset', 'fast',  # Encoding preset
                    temp_clip
                ]
            subprocess.run(extract_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            temp_clips.append(temp_clip)
        temp_list_file = os.path.join(temp_dir, 'input.txt')
        
        # Write the list of input section files to a temporary file so we can use ffmpeg concat filter
        with open(temp_list_file, 'w') as f:
            for clip in temp_clips:
                f.write(f"file '{clip}'\n")
        # concatenate all clips into a full video
        concat_cmd = [
            'ffmpeg', 
            '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_list_file,
            '-c:v', 'libx264',  
            '-c:a', 'aac',      
            '-preset', 'fast',  
            output_video_filename
        ]
        print(concat_cmd)
        subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Clean up temporary video clips
        for temp_clip in temp_clips:
            try:
                os.remove(temp_clip)
                print(f"Deleted temporary clip: {temp_clip}")
            except Exception as e:
                print(f"Error deleting temporary clip: {temp_clip}. Error: {e}")
    
    return output_video_filename