import numpy as np
import cv2
import math
from os.path import join
target_frames = 300
target_resolution = (1920,1080)
output_dir = 'output'
extension='png'


def video_to_images(input_path, target_frames, target_resolution, output_dir, extension='png', sg=None):
  cap = cv2.VideoCapture(input_path)

  fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
  frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  cap_w, cap_h = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

  needs_resize = target_resolution is not None and (cap_w, cap_h) != target_resolution and (cap_h, cap_w) != target_resolution
  if needs_resize:
      print(f"This file will be resized to {target_resolution[0]}, {target_resolution[1]}")
  elif cap_w != target_resolution:
      print("Image dimensions match with rotation, not resizing")
  frame_skip = math.floor(frame_count/target_frames)
  print(f"Target frame skip is {frame_skip}")

  i = 0
  count = 0
  err=False
  while(cap.isOpened()):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
      break
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if needs_resize:
      frame = cv2.resize(frame, target_resolution)

    path = join(output_dir, f'{count:04d}.{extension}')
    print(f"Writing to {path}")
    cv2.imwrite(path,frame)
    count += 1
    if sg:
      if not sg.one_line_progress_meter("Export progress",count, target_frames):
        err = True
        break
    i += frame_skip
    if frame_skip >= frame_count:
      break
    if cv2.waitKey(1) & 0xFF == ord('q'):
      err=True
      break

  cap.release()
  return err
