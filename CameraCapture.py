import cv2
from abc import ABC, abstractmethod
from typing import Any

class CameraCapture(ABC):
    @abstractmethod
    def capture_frame(self) -> (int, Any):
        pass

    @abstractmethod
    def get_frame_width(self) -> int:
        pass

    @abstractmethod
    def get_frame_height(self) -> int:
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

class CVCameraCapture(CameraCapture):
    def __init__(self, camera_index: int):
        self._camera_index: int = camera_index
        self._cam: int = None

    def init(self):
        if not self._cam:
            self._cam = cv2.VideoCapture(self._camera_index)
        return self

    def deinit(self):
        if self._cam:
            self._cam.release()
            self._cam = None

    def capture_frame(self) -> (int, Any):
        if not self._cam:
            raise Exception("Camera object not initialized")
        return self._cam.read()

    def get_frame_width(self) -> int:
        if not self._cam:
            raise Exception("Camera object not initialized")
        return int(self._cam.get(cv2.CAP_PROP_FRAME_WIDTH))

    def get_frame_height(self) -> int:
        if not self._cam:
            raise Exception("Camera object not initialized")
        return int(self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
