import numpy as np
import cv2
import os
import torch
import subprocess
from facenet_pytorch import MTCNN, InceptionResnetV1
# infrastructure
import json
from types import MethodType

def load_clips(clips_dir_path: str = None) -> list[str]: 
  """Loads in input video file path names for processing.

  Args:
      clip_dir (str, optional): Path name for the directory in which the input video files are located. 
      Defaults to None and uses the current working directory with a 'videos' subfolder if not provided.
  """
  if clips_dir_path is None:
    clips_dir_path = os.path.join(os.getcwd(), "Input Clips" + os.sep) # TODO: maybe do more sophisticated checking for a videos folder? Like instead error out if not found
  clips = []
  for root, dirs, files in os.walk(clips_dir_path): 
    for file in files:
      path = os.path.join(root, file)
      clips.append(path)
  return clips 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces_cascade(clip_path: str, should_annotate:bool = False, output_dir:str = ""):
  frames = []
  cap = cv2.VideoCapture(clip_path)

  fps = cap.get(cv2.CAP_PROP_FPS)

  output_title = os.path.join(output_dir, os.path.basename(clip_path).split(".")[0] + ".mp4")
  print(output_title)

  # Get the width and height of the frames
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  # Create a VideoWriter object to save the output video
  # output_video = cv2.VideoWriter(output_title, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
  
  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      print("Finish! Exiting...")
      break
    # grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    frames.append(np.array([]) if len(faces) == 0 else faces)

    for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # this function writes to the frame object

    # output_video.write(frame)
  cap.release()
  
  ffmpeg_command = [
    "ffmpeg",
    "-i", output_title,
    "-i", clip_path,
    "-c:v", "copy",
    "-c:a", "aac",
    "-strict", "experimental",
    "-map", "0:v:0",
    "-map", "1:a:0",
    output_title + "f"
  ]

  subprocess.run(ffmpeg_command)
  
  return frames


if __name__ == '__main__':
  clips = load_clips()
  print(os.path.join(os.getcwd(), "output" + os.sep))
  for clip in clips:
    frames = detect_faces_cascade(clip, True, os.path.join(os.getcwd(), "output" + os.sep))
    print(len(frames))