import numpy as np
import cv2

from metavision_sdk_core import BaseFrameGenerationAlgorithm
from metavision_sdk_stream import Camera, CameraStreamSlicer, SliceCondition
from metavision_sdk_ui import EventLoop

camera = Camera.from_first_available()

delta_t_us = 10000
slice_condition = SliceCondition.make_n_us(delta_t_us)
slicer = CameraStreamSlicer(camera.move(), slice_condition)

width = slicer.camera().width()
height = slicer.camera().height()
frame = np.zeros((height, width, 3), np.uint8)

for slice in slicer:
    EventLoop.poll_and_dispatch()
    print(f"ts: {slice.t}, new slice of {slice.events.size} events")

    BaseFrameGenerationAlgorithm.generate_frame(slice.events, frame)
    cv2.imshow('preview', frame)
    cv2.waitKey(1)

# cv2.destroyAllWindows()