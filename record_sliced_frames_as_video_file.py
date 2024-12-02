import numpy as np
import cv2

from metavision_sdk_core import BaseFrameGenerationAlgorithm
from metavision_sdk_stream import Camera, CameraStreamSlicer, SliceCondition
from metavision_sdk_ui import EventLoop

# Setup.
camera = Camera.from_first_available()

capture_fps = 1000
delta_t_us = int(1000000/capture_fps)
slice_condition = SliceCondition.make_n_us(delta_t_us)
slicer = CameraStreamSlicer(camera.move(), slice_condition)

capture_secs = 1.0
num_frames = int(capture_fps*capture_secs)
width = slicer.camera().width()
height = slicer.camera().height()
ch = 3  # B, G, R
frames = np.zeros((num_frames, height, width, ch), np.uint8)  # ←メモリ食うよ！
# /Setup.

# Capturing, buffering in mem.
i = 0
for slice in slicer:
    EventLoop.poll_and_dispatch()
    print(f"i: {i}, ts: {slice.t}, new slice of {slice.events.size} events")

    BaseFrameGenerationAlgorithm.generate_frame(slice.events, frames[i])
    # cv2.imshow('preview', frames[i])  # ←60fps以上を表示させようとすると遅延していく
    # cv2.waitKey(1)

    i += 1
    if i == num_frames:
        break

# cv2.destroyAllWindows()
# /Capturing, buffering in mem.

# Recording, post proc.
codec = 'H264'
video_file_path = "./captured.mp4"
video_fps = 60.0
fourcc = cv2.VideoWriter_fourcc(*codec)
writer = cv2.VideoWriter(video_file_path, fourcc, video_fps, (width, height))

for i in range(num_frames):
    writer.write(frames[i])

writer.release()
# /Recording, post proc.
