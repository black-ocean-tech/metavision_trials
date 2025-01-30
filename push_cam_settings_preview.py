from metavision_sdk_core import BaseFrameGenerationAlgorithm
from metavision_sdk_stream import Camera, CameraStreamSlicer, SliceCondition
from metavision_sdk_ui import EventLoop

camera = Camera.from_first_available()

# fetch, push cam settings
import json

bias_diff = 300
bias_diff_off = 150
bias_diff_on = 450

camera.save("./default_settings.json")
with open("./default_settings.json", "r") as _:
    dict_ = json.load(_)
print(dict_["ll_biases_state"])

dict_["ll_biases_state"]["bias"][0]["value"] = bias_diff
dict_["ll_biases_state"]["bias"][1]["value"] = bias_diff_off
dict_["ll_biases_state"]["bias"][2]["value"] = bias_diff_on

with open("./edited_settings.json", "w") as _:
    json.dump(dict_, _)
camera.load("./edited_settings.json")
print(dict_["ll_biases_state"])
# /fetch, push cam settings

# setup
import numpy as np

capture_fps = 100

delta_t_us = int(10**6/capture_fps)
slice_condition = SliceCondition.make_n_us(delta_t_us)
slicer = CameraStreamSlicer(camera.move(), slice_condition)

width = slicer.camera().width()
height = slicer.camera().height()
frame = np.zeros((height, width, 3), np.uint8)
# /setup

# preview
import cv2

for slice in slicer:
    EventLoop.poll_and_dispatch()
    print(f"ts: {slice.t}, new slice of {slice.events.size} events")

    BaseFrameGenerationAlgorithm.generate_frame(slice.events, frame)
    cv2.imshow('preview', frame)
    cv2.waitKey(1)

# cv2.destroyAllWindows()

# /preview

