import cv2
from typing import Any
from datetime import datetime

class CameraCaptureFilter:
    def __init__(self, min_diff: float, active_time_delta_s: float):
        self._min_diff: float = min_diff
        self._active_time_delta_s: float = active_time_delta_s
        self._last_capture_time = None
        self._last_frame = None

    def filter(self, frame: Any) -> bool:
        if frame is None:
            return False

        # This is the initial capture, there is nothing to compare it against.
        # We will return it anyway since we want to see the initial look.
        if self._last_frame is None:
            self._last_frame = frame
            return True

        r_diff, g_diff, b_diff, _ = cv2.mean(cv2.absdiff(self._last_frame, frame))
        total_diff = r_diff + g_diff + b_diff

        self._last_frame = frame
        return self._decide(total_diff=total_diff)
    
    def _decide(self, total_diff: float) -> bool:
        if total_diff > self._min_diff:
            self._last_capture_time = datetime.now()
            return True

        if self._last_capture_time is None:
            return False

        time_since_last = datetime.now() - self._last_capture_time
        return time_since_last.total_seconds() < self._active_time_delta_s