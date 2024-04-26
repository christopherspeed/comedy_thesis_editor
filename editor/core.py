import numpy as np
from dataclasses import dataclass

class Edit:
    def __init__(self, name: str) -> None:
        self.name = name # name of the edit
        self.edit_list: "list[VideoSegment]" = []
        self.duration = -1 # needs to be updated in the process of getting the clips

@dataclass
class VideoSegment:
    filename: str
    start: int
    end: int
    
@dataclass
class MetaClipData:
    filename: str
    normalized_detection_areas: np.ndarray
    avg_normalized_area: float # the average normalized detected face area 
    clip_height: int
    clip_width: int