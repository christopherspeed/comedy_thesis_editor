import numpy as np
import cv2 
from tqdm import tqdm
from typing import Literal

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces_cascade(clip_path: str, should_annotate:bool = False, output_dir:str = ""):
    frames = []
    cap = cv2.VideoCapture(clip_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    # output_title = os.path.join(output_dir, os.path.basename(clip_path).split(".")[0] + ".mp4")
    # print(output_title)
    print(clip_path)
    # Get the width and height of the frames
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Create a VideoWriter object to save the output video
    # output_video = cv2.VideoWriter(output_title, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    
    # display progress
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    with tqdm(total=frame_count) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Finish! Exiting...")
                break
            # grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            frames.append(np.array([]) if len(faces) == 0 else faces)
            pbar.update(1)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # this function writes to the frame object

        # output_video.write(frame)
    cap.release()
    
    # ffmpeg_command = [
    #     "ffmpeg",
    #     "-i", output_title,
    #     "-i", clip_path,
    #     "-c:v", "copy",
    #     "-c:a", "aac",
    #     "-strict", "experimental",
    #     "-map", "0:v:0",
    #     "-map", "1:a:0",
    #     output_title + "f"
    # ]

    # subprocess.run(ffmpeg_command)
    
    return frames

def detect_faces(clips: "list[str]", method: Literal["haar", "facenet"]):
    faces = []
    if method == 'haar':
        faces = [{"filename":clip, "detections": detect_faces_cascade(clip)} for clip in clips]
    elif method == "facenet":
        print("Not implemented yet.")
    else:
        raise ValueError("Invalid method type specified. Supported methods are 'haar' and 'facenet'.")
    return faces