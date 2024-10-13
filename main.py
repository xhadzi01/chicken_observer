from CameraExecutor import CameraExecutor

def main():
    cc = CameraExecutor(camera_index=0, min_diff=10.0, active_time_delta_s=10.0, debug_mode=False)
    cc.start_capture()

if __name__ == "__main__":
    main()