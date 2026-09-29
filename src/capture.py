from picamera2 import Picamera2
import cv2
import numpy as np

class IRCamera:
    def __init__(self, cfg):
        self.cfg = cfg
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": (cfg['resolution_width'], cfg['resolution_height']), "format": "RGB888"},
            controls={"AwbEnable": False, "AeEnable": True}
        )
        self.picam2.configure(config)
        self.picam2.start()
        
    def capture_frame(self):
        frame = self.picam2.capture_array()
        return frame

    def capture_and_resize(self, input_size):
        frame = self.capture_frame()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        resized = cv2.resize(frame_bgr, (input_size, input_size))
        img = resized.astype(np.float32) / 255.0
        return frame_bgr, img
