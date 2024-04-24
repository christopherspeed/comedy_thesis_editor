import numpy as np
import os
from collections import deque
from editor.core import Edit, VideoSegment, MetaClipData
from processing.load import save_edit
from processing.features import get_best_new_clip, is_face_visible

    
def edit_random(edit_start_time: int=0, num_cuts=0):
    pass

def edit_simple(
    current_edit:Edit, 
    clips_and_annotations: "list[MetaClipData]",
    starting_clip:MetaClipData, threshold_frames:int = 5,
    cut_frequency_threshold_frames = 60,
    edit_start_time: int=0,
    strictness_amt: float=0.5,
    should_save=True
    ) -> Edit:
    
    new_edit = current_edit
    new_edit_list: "list[VideoSegment]" = []
    
    # main edit loop
    frames_remaining = threshold_frames
    current_clip = starting_clip
    clip_start = edit_start_time
    cut_allowed_time_remaining = cut_frequency_threshold_frames
    
    for t in range(edit_start_time, current_edit.duration): # TODO: ensure duration isn't -1
        # swap if performer's face isn't visible for threshold # of frames
        if not is_face_visible(t, current_clip, strictness_amt): frames_remaining -= 1
        else: frames_remaining = threshold_frames # reset if face returns
        
        # cut successfuly triggered
        if frames_remaining == 0 and cut_allowed_time_remaining == cut_frequency_threshold_frames: # enough frames have elapsed and we haven't cut too recently
            frames_remaining = threshold_frames
            clip_start = t #TODO may have off-by-one error
            new_clip = get_best_new_clip(t, current_clip, threshold_frames, clips_and_annotations)
            new_edit_list.append(VideoSegment(current_clip, start=clip_start, end=t)) # TODO: maybe adjust in cases where we can't cut
            current_clip = new_clip
            cut_allowed_time_remaining = 0 # reset counter for how frequently we can cut
            continue # skip the increment for our counter
        cut_allowed_time_remaining = cut_allowed_time_remaining + 1 if cut_allowed_time_remaining != cut_frequency_threshold_frames else cut_frequency_threshold_frames

    if edit_start_time != 0 and current_edit.duration != -1: # we're modifying a prior edit
        new_edit.edit_list = overwrite(current_edit.edit_list, new_edit_list, duration=current_edit.duration)
    else:
        new_edit.edit_list = new_edit_list
    
    # save for statefulness
    if should_save:
        save_edit(new_edit)
        
    return new_edit
    
        

def edit_complex(edit_start_time: int=0, should_save=True):
    pass    
    
def overwrite(current_edit_list: "list[VideoSegment]",
              new_edit_list: "list[VideoSegment]",
              duration: int) -> "list[VideoSegment]":
    output_edit_list: "list[VideoSegment]" = []
    
    start_clip, end_clip = new_edit_list[0], new_edit_list[-1]
    # print(start_clip, end_clip)
    
    # print("Initial List: ", current_edit_list)
    # print("Overwrite List: ", new_edit_list)
    # integrate the start + all except end
    for i in range(len(current_edit_list)):
        current_clip = current_edit_list[i]
        # current clip is earlier than any of the overwrites
        if current_clip.end < start_clip.start:
            output_edit_list.append(current_clip)
        # current clip is after any of the overwrites
        elif current_clip.start > end_clip.end:
            output_edit_list.append(current_clip)
        # current clip fully contains the proposed start clip:
        elif current_clip.start < start_clip.start and start_clip.end <= current_clip.end:
            combined_clip = VideoSegment(current_clip.filename, start=current_clip.start, end=start_clip.start-1)
            output_edit_list.append(combined_clip)
            if len(new_edit_list) == 1:
                output_edit_list.append(start_clip) # same as last clip
                output_edit_list.append(VideoSegment(current_clip.filename, start=start_clip.end+1, end=current_clip.end)) # same as last clip
            else:
                output_edit_list.extend(new_edit_list)
        # current clip is completely contained by start clip
        elif start_clip.start == current_clip.start and start_clip.end > current_clip.end:
            output_edit_list.append(start_clip)
            while i != len(current_edit_list) - 2:
                next_clip = current_edit_list[i+1]
                if start_clip.end > next_clip.start and start_clip.end < next_clip.end:
                    output_edit_list.append(VideoSegment(next_clip.filename, start_clip.end + 1, next_clip.end))
                    break
        # current clip partially overlaps
        elif start_clip.start > current_clip.start and start_clip.end > current_clip.end:
            print()
            output_edit_list.append(VideoSegment(current_clip.filename, start=current_clip.start, end=start_clip.start - 1)) # same as last clip
            output_edit_list.append(start_clip)
            while i != len(current_edit_list) - 2:
                next_clip = current_edit_list[i+1]
                if start_clip.end > next_clip.start and start_clip.end < next_clip.end:
                    output_edit_list.append(VideoSegment(next_clip.filename, start_clip.end, next_clip.end))
                    break
        # elif end_clip.end > current_clip.start and end_clip.end < current_clip.end:
        #     output_edit_list.append(start_clip)
        #     output_edit_list.append(VideoSegment(current_clip.filename, start=end_clip.start + 1, end=current_clip.end))
    
    return output_edit_list
    
if __name__ == '__main__':
    # edit = Edit("test")
    # edit.duration = 32
    edit_list = [VideoSegment("video 1", 0, 15), VideoSegment("Video 2", 15, 32)]
    print(overwrite(edit_list, [VideoSegment("Clip1", 8, 27)]))