import os
import json
import pickle
from editor.core import Edit, MetaClipData, VideoSegment
from processing.features import process_clips

def setup_editor(new_edit_title: str, new_annotation_title:str, clips_src_dir:str, previous_edit_filename: str="", previous_annotation_filename: str=""):
    clips = get_input_clips(clips_src_dir)
   
    if previous_annotation_filename == "":
        print("Newly processing annotations")
        annotations = process_clips(clips)
        save_annotations(new_annotation_title, annotations)
    else:
        print("Loading Prior Annotations")
        annotations = load_annotations(previous_annotation_filename)
        
    if previous_edit_filename == "":
        print("Previous Edit does not exist. Creating new Edit instance")
        edit = Edit(new_edit_title)
        edit.duration = len(annotations[0].normalized_detection_areas)
        # save this edit as state initialization
        save_edit(edit)
    else:
        print("Previous Edit exists! Loading it from disk.")
        edit = load_edit(previous_edit_filename) # duration, name, etc. should be properly initialized
        
    return edit, annotations


def get_input_clips(clip_src_dir: str) -> "list[str]":
    clips = []
    for root, _, files in os.walk(clip_src_dir): 
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".MOV") or path.endswith(".mp4"): clips.append(path)
    return clips


# def save_current_edit(current_video_edit: "list[dict]", filename_to_save_to: str):
#     with open(filename_to_save_to, 'w') as f:
#         json.dump(current_video_edit, f, ensure_ascii=False)
#     print("Edit Data Saved")

# def load_previous_edit(filename_to_load_from: str):
#     with open(filename_to_load_from, 'r') as f:
#         data = json.load(f)
#     print("Previous Edit Data Loaded")
#     return data

def save_edit(current_video_edit: Edit):
    filename = current_video_edit.name + ".pkl"
    print(f"Saving current edit to {filename}")
    with open(filename, 'wb') as f:
        pickle.dump(current_video_edit, f)
    print("Edit Data Saved")

    # Get the file size
    file_size = os.path.getsize(filename)
    print(f"File size of {filename}: {file_size} bytes")


def load_edit(previous_video_edit_name: str) -> Edit:
    filename = previous_video_edit_name + ".pkl"
    print(f"Loading previous edit from {filename}")
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print("Previous Edit Data Loaded")
    return data

def save_annotations(annotation_filename_for_saving: str,annotations: "list[MetaClipData]"):
    filename = annotation_filename_for_saving + ".pkl"
    print(f"Saving clip annotations to {filename}")
    with open(filename, 'wb') as f:
        pickle.dump(annotations, f)
    print("Annotation Data Saved")

    # Get the file size
    file_size = os.path.getsize(filename)
    print(f"File size of {filename}: {file_size} bytes")
    
def load_annotations(annotation_filename: str) -> "list[MetaClipData]":
    filename = annotation_filename + ".pkl"
    print(f"Saving clip annotations to {filename}")
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print("Annotation Data Loaded")
    return data
    
    