import cv2
from abc import ABC
from typing import Any
from time import strftime

from CameraCaptureFilter import CameraCaptureFilter
from CameraCaptureWritter import CameraCaptureWritter, CVCameraCaptureWritter
from CameraCapture import CameraCapture, CVCameraCapture
from SignalHandler import SignalHandler

class CameraExecutor:
    def __init__(self, camera_index: int, min_diff: float, active_time_delta_s: float, debug_mode: bool = False):
        # video capture
        self._camera_index: int = camera_index
        # video filtering
        self._filter: CameraCaptureFilter = CameraCaptureFilter(min_diff=min_diff, active_time_delta_s=active_time_delta_s)
        # utils
        self._debug_mode: bool = debug_mode

    def start_capture(self):
        with CVCameraCapture(camera_index=self._camera_index) as cam:        
            # Get the default frame width and height
            frame_width = cam.get_frame_width()
            frame_height = cam.get_frame_height()
            with CVCameraCaptureWritter(frame_width=frame_width, frame_height=frame_height) as writter, SignalHandler() as handler:
                while not handler.is_signaled():
                    ret, frame = cam.capture_frame()

                    # Write the frame to the output file
                    if self._filter.filter(frame=frame):
                        cv2.putText(frame, strftime("%H:%M:%S"), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2 ,cv2.LINE_AA)
                        writter.write_frame(frame=frame)

                        # Debug - Display the captured frame
                        if self._debug_mode:
                            cv2.imshow('Camera', frame)

                    # Press 'q' to exit the loop
                    if cv2.waitKey(1) == ord('q'):
                        handler.signal()

                cv2.destroyAllWindows()
