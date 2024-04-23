import numpy as np
import os
from editor.core import Edit, VideoSegment, MetaClipData

from processing.features import get_best_new_clip, is_face_visible

    
def edit_random(edit_start_time: int=0, num_cuts=0):
    pass

def edit_simple(current_edit:Edit, clips_and_annotations: "list[MetaClipData]", starting_clip:MetaClipData, threshold_frames:int = 5, edit_start_time: int=0, should_save=True):
    new_edit = []
    # main edit loop
    frames_remaining = threshold_frames
    current_clip = starting_clip
    clip_start = edit_start_time
    for t in range(edit_start_time, current_edit.duration): # TODO: ensure duration isn't -1
        # swap if performer's face isn't visible for threshold # of frames
        if not is_face_visible(t, current_clip): frames_remaining -= 1
        else: frames_remaining = threshold_frames # reset if face returns
        
        if frames_remaining == 0:
            frames_remaining = threshold_frames
            clip_start = t # may have off-by-one error
            new_edit.append(VideoSegment(current_clip, start=clip_start, end=t)) # TODO: maybe adjust in cases where we can't cut
            current_clip = get_best_new_clip(t, threshold_frames, clips_and_annotations)
            
    
    
    return new_edit
    
        

def edit_complex(edit_start_time: int=0, should_save=True):
    pass    
    
def overwrite(current_edit: Edit, clip: str, start, end) -> "list[dict]":
    edit_list: "list[VideoSegment]" = current_edit.edit_list
    duration: int = current_edit.duration
    if len(edit_list) == 0:
        raise ValueError("Invalid zero-length input edit sequence. An edit paradigm must be applied before overwriting is permitted.")
    if start < 0 or start >= duration:
        raise ValueError(f"Start time {start} not within sequence bounds.")
    if end < 0 or end >= duration:
        raise ValueError(f"End time {end} not within sequence bounds.")
    new_edit = []
    
    for i in range(len(edit_list)):
        clip = edit_list[i]
        clip_start, clip_end = clip.start, clip.end
        print(clip_start, clip_end)
    
    return new_edit
    
if __name__ == '__main__':
    edit = Edit("test")
    edit.duration = 32
    edit.edit_list = [VideoSegment("video 1", 0, 15), VideoSegment("Video 2", 15, 32)]
    overwrite(edit, "Clip1", 8, 27)