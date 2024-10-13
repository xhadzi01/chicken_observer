import cv2
from abc import ABC
from typing import Any
from CameraCaptureFilter import CameraCaptureFilter
from CameraCaptureWritter import CameraCaptureWritter, CVCameraCaptureWritter
from CameraCapture import CameraCapture, CVCameraCapture

class CameraExecutor:
    def __init__(self, camera_index: int):
        # video capture
        self._camera_index: int = camera_index
        # video filtering
        self._filter: CameraCaptureFilter = CameraCaptureFilter()

    def start_capture(self):
        with CVCameraCapture(camera_index=self._camera_index) as cam:        
            # Get the default frame width and height
            frame_width = cam.get_frame_width()
            frame_height = cam.get_frame_height()
            with CVCameraCaptureWritter(frame_width=frame_width, frame_height=frame_height) as writter:
                while True:
                    ret, frame = cam.capture_frame()

                    # Write the frame to the output file
                    if self._filter.filter(frame=frame):
                        writter.write_frame(frame)

                    # Display the captured frame
                    cv2.imshow('Camera', frame)

                    # Press 'q' to exit the loop
                    if cv2.waitKey(1) == ord('q'):
                        break

                cv2.destroyAllWindows()
