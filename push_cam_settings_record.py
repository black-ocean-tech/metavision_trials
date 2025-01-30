from metavision_sdk_core import BaseFrameGenerationAlgorithm
from metavision_sdk_stream import Camera, CameraStreamSlicer, SliceCondition
from metavision_sdk_ui import EventLoop

camera = Camera.from_first_available()

# fetch, push cam settings
import json

bias_diff = 299  # recommended to not change
bias_diff_off = 100  # 100-234
bias_diff_on = 499  # 374-499
bias_fo = 1447
bias_hpf = 1448
bias_pr = 1250
bias_refr = 1500
roi_x = 0
roi_y = 120
roi_w = 640
roi_h = 240

camera.save("./default_settings.json")
with open("./default_settings.json", "r") as _:
    dict_ = json.load(_)
print(dict_["ll_biases_state"])
print(dict_["roi_state"])

dict_["ll_biases_state"]["bias"][0]["value"] = bias_diff
dict_["ll_biases_state"]["bias"][1]["value"] = bias_diff_off
dict_["ll_biases_state"]["bias"][2]["value"] = bias_diff_on
dict_["ll_biases_state"]["bias"][3]["value"] = bias_fo
dict_["ll_biases_state"]["bias"][4]["value"] = bias_hpf
dict_["ll_biases_state"]["bias"][5]["value"] = bias_pr
dict_["ll_biases_state"]["bias"][6]["value"] = bias_refr
dict_["roi_state"]["window"] = {
      "x": roi_x,
      "y": roi_y,
      "width": roi_w,
      "height": roi_h
     }
dict_["roi_state"]["enabled"] = True

with open("./edited_settings.json", "w") as _:
    json.dump(dict_, _)
print(dict_["ll_biases_state"])
print(dict_["roi_state"])
camera.load("./edited_settings.json")
# /fetch, push cam settings

# Setup.
import numpy as np

capture_fps = 20000
capture_secs = 0.5

delta_t_us = int(10**6/capture_fps)
slice_condition = SliceCondition.make_n_us(delta_t_us)
slicer = CameraStreamSlicer(camera.move(), slice_condition)

num_frames = int(capture_fps*capture_secs)
width = slicer.camera().width()
height = slicer.camera().height()
ch = 3  # B, G, R
frames = np.zeros((num_frames, height, width, ch), np.uint8)  # ←動画全キャッシュするのでメモリ食うよ！
# /Setup.

# Capturing, buffering in mem.
i = 0
for slice in slicer:
    EventLoop.poll_and_dispatch()
    # print(f"i: {i}, ts: {slice.t}, new slice of {slice.events.size} events")

    BaseFrameGenerationAlgorithm.generate_frame(slice.events, frames[i])
    # cv2.imshow('preview', frames[i])  # ←60fps以上を表示させようとすると遅延していく
    # cv2.waitKey(1)

    i += 1
    if i == num_frames:
        break

# cv2.destroyAllWindows()
# /Capturing, buffering in mem.

# Recording, post proc.
import cv2

codec = 'H264'
video_file_path = "./captured.mp4"
video_fps = 60.0

fourcc = cv2.VideoWriter_fourcc(*codec)
writer = cv2.VideoWriter(video_file_path, fourcc, video_fps, (width, height))

for i in range(num_frames):
    writer.write(frames[i])

writer.release()
# /Recording, post proc.
