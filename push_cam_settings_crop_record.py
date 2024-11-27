from metavision_sdk_core import BaseFrameGenerationAlgorithm
from metavision_sdk_stream import Camera, CameraStreamSlicer, SliceCondition
from metavision_sdk_ui import EventLoop

camera = Camera.from_first_available()

# fetch, push cam settings
import json

bias_diff = 300
bias_diff_off = 200
bias_diff_on = 400
roi_x = 160
roi_y = 120
roi_w = 320
roi_h = 240

camera.save("./default_settings.json")
with open("./default_settings.json", "r") as _:
    dict_ = json.load(_)

dict_["ll_biases_state"]["bias"][0]["value"] = bias_diff
dict_["ll_biases_state"]["bias"][1]["value"] = bias_diff_off
dict_["ll_biases_state"]["bias"][2]["value"] = bias_diff_on
# print(dict_["ll_biases_state"]["bias"])

dict_["roi_state"]["window"] = {
      "x": roi_x,
      "y": roi_y,
      "width": roi_w,
      "height": roi_h
     }
dict_["roi_state"]["enabled"] = True
# print(dict_["roi_state"])

with open("./edited_settings.json", "w") as _:
    json.dump(dict_, _)
camera.load("./edited_settings.json")
# /fetch, push cam settings

# setup
import numpy as np

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
# /setup

# capturing, buffering in mem
import cv2

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
# /capturing, buffering in mem

# croping, recording, post proc
codec = 'H264'
video_file_path = "./captured.mp4"
video_fps = 60.0
fourcc = cv2.VideoWriter_fourcc(*codec)
writer = cv2.VideoWriter(video_file_path, fourcc, video_fps, (roi_w, roi_h))

for i in range(num_frames):
    cropped = frames[i][roi_y: roi_y + roi_h, roi_x: roi_x + roi_w, :]
    # print(cropped.shape)
    writer.write(cropped)

writer.release()
# /croping, recording, post proc
