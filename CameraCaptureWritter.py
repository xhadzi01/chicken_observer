import cv2
from abc import ABC, abstractmethod
from typing import Any

class CameraCaptureWritter(ABC):
    @abstractmethod
    def write_frame(self, frame: Any):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def deinit(self):
        pass
    
    def __enter__(self):
        return self.init()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.deinit()

class CVCameraCaptureWritter(CameraCaptureWritter):
    def __init__(self, frame_width: int, frame_height: int):
        self._frame_width: int = frame_width
        self._frame_height: int = frame_height
        self._fourcc = None
        self._out = None

    def init(self):
        if not self._out: 
            self._fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self._out = cv2.VideoWriter('output.mp4', self._fourcc, 20.0, (self._frame_width, self._frame_height))
        return self

    def deinit(self):
        if self._out: 
            self._out.release()
            self._out = None
            self._fourcc = None

    def write_frame(self, frame: Any):
        if not self._out:
            raise Exception("Writter object not initialized")
        self._out.write(frame)
