import numpy as np
import cv2 
from tqdm import tqdm
from typing import Literal
from editor.core import MetaClipData

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def process_clips(clips: "list[str]", method: str='haar') -> "list[MetaClipData]":
    annotations = detect_faces(clips, method)
    return annotations

def detect_faces_cascade(clip_path: str, should_annotate:bool = False, output_dir:str = ""):
    
    cap = cv2.VideoCapture(clip_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # print(output_title)
    print(clip_path)
    # Get the width and height of the frames
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # display progress
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames = np.zeros(frame_count)
    frame_index = 0
    
    with tqdm(total=frame_count) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Finish! Exiting...")
                break
            # grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5) # assume 1 detection
            if len(faces) != 0:
                x, y, w, h = faces[0]
                w_norm = w / frame_width
                h_norm = h / frame_height

            frames[frame_index] = 0.0 if len(faces) == 0 else w_norm * h_norm
            frame_index += 1
            pbar.update(1)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # this function writes to the frame object

        # output_video.write(frame)
    cap.release()
    
    avg_normalized_area = np.mean(frames != 0) # average when faces are actually present
    
    return frames, frame_width, frame_height, avg_normalized_area

def detect_faces(clips: "list[str]", method: Literal["haar", "facenet"]):
    print("Clips to process: ", clips)
    faces = []
    if method == 'haar':
        for clip in clips:
            normalized_detection_areas, width, height, avg_normalized_area = detect_faces_cascade(clip)
            faces.append(MetaClipData(clip, normalized_detection_areas, avg_normalized_area, height, width))
    elif method == "facenet":
        print("Not implemented yet.")
    else:
        raise ValueError("Invalid method type specified. Supported methods are 'haar' and 'facenet'.")
    return faces

############## Face Detection Comparison Utilities ############################

def get_best_new_clip(start_frame: int, transitioned_clip: MetaClipData, threshold: int, detections: "list[MetaClipData]") -> MetaClipData:
    clip_choices = [(clip.normalized_detection_areas[start_frame], clip) for clip in detections if clip != transitioned_clip] # exclude the clip we're transitioning from? -> what if no others are better?
    
    # initialize and look for potentially better options
    max_area = clip_choices[0][0]
    best_clip = clip_choices[0][1]
    
    for area, clip in clip_choices:
        if area > max_area:
            best_clip = clip
            max_area = area
    
    return best_clip

def is_face_visible(frame: int, clip: MetaClipData, strictness: float) -> bool:
    detected_area: int = clip.normalized_detection_areas[frame]
    ratio = float(detected_area) / float(clip.avg_normalized_area)
    return ratio > strictness
    