import os
import json


def get_input_clips(clip_src_dir: str) -> "list[str]":
    clips = []
    for root, _, files in os.walk(clip_src_dir): 
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".MOV") or path.endswith(".mp4"): clips.append(path)
    return clips

def save_current_edit(current_video_edit: "list[dict]", filename_to_save_to: str):
    with open(filename_to_save_to, 'w') as f:
        json.dump(current_video_edit, f, ensure_ascii=False)
    print("Edit Data Saved")

def load_previous_edit(filename_to_load_from: str):
    with open(filename_to_load_from, 'r') as f:
        data = json.load(f)
    print("Previous Edit Data Loaded")
    return data