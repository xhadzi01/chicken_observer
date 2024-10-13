from CameraExecutor import CameraExecutor

def main():
    cc = CameraExecutor(camera_index=0)
    cc.start_capture()

if __name__ == "__main__":
    main()