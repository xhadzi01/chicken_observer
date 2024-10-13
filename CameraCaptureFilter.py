from typing import Any

class CameraCaptureFilter:
    def __init__(self):
        self._last_frame = None

    def filter(self, frame: Any) -> bool:
        # TODO: There will be filtering
        return True