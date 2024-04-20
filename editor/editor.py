import numpy 
import os

from dataclasses import dataclass

class Edit:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edit_list: "list[VideoSegment]" = []
        self.duration = -1 # needs to be updated in the process of getting the clips

@dataclass
class VideoSegment:
    filename: str
    start: int
    end: int
    
def edit_random(edit_start_time: int=0, num_cuts=0):
    pass

def edit_simple(edit_start_time: int=0):
    pass

def edit_complex(edit_start_time: int=0):
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