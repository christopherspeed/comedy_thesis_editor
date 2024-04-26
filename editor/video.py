import subprocess
import tempfile
import os
import uuid
from tqdm import tqdm

from editor.core import VideoSegment

def assemble(clips: "list[VideoSegment]", number_of_clips: int, fps: int, verbose=False, output_video_filename="Output_Video.mp4") -> str:
    if verbose:
        print("Edits to apply:")
        for clip in clips[:number_of_clips]:
            print(clip)
    print(output_video_filename)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print("--- Beginning Video Segment Assembly ---")
        # print(f"Temporary Directory: {temp_dir}")        
        temp_clips = []
   
        for i, clip in enumerate(clips):
            clip_filename = clip.filename
            start, end =  round((clip.start / fps) * fps) / fps, round((clip.end / fps) * fps) / fps
            # remove ending filename, make ensure that we can take multiple sections of the same clip
            temp_clip = os.path.join(temp_dir, f'{clip_filename[:-4]}_{str(uuid.uuid4())}.mp4')
            if verbose:
                print(f"Current Segment -> file: {clip_filename} start: {start} end: {end}")
                print(f"Temporary clip {temp_clip} with duration {end-start + 1} created...")
            
            if i == len(clips) - 1: # final clip
                print("Final Clip in Sequence is being Extracted...")
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
            print(extract_command)
            subprocess.run(extract_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            temp_clips.append(temp_clip)
            if i == number_of_clips - 1:
                print(f"Early exiting with {i + 1} clips processed")
                break
        
        temp_list_file = os.path.join(temp_dir, 'input.txt')
        print("Temporary List File: ", temp_list_file)
        
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
        print("About to attempt concatenation...")
        subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        
        # Clean up temporary video clips
        for temp_clip in temp_clips:
            try:
                os.remove(temp_clip)
                print(f"Deleted temporary clip: {temp_clip}")
            except Exception as e:
                print(f"Error deleting temporary clip: {temp_clip}. Error: {e}")
    
    print("--- Video Segment Assembly Completed ---") 
    return output_video_filename
