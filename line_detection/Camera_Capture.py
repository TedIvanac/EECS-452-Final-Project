import cv2 as cv
import numpy as np

from Image_Process import Image_Process
from Directions import Directions

CAMERA_DIR = 4
FPS = 15
DELAY = int(1000/FPS)

class Camera_Capture():
    
    def __init__(self):
        self.cap = cv.VideoCapture(CAMERA_DIR)
        self.image_processor = Image_Process()
        self.robot_commands = Directions()

    # Return boolean based 
    def _camera_opened(self):
        return self.cap.isOpened()

    def _capture_frame(self):
        frame_count = 0
        prev_frame = np.ones((480, 640), dtype=np.uint8)*255

        while True:
            ret, frame = self.cap.read()
            if not ret:
                return

            cv.imshow('Default', frame)
            binary = self.image_processor._gray2binary(frame)
            self.image_processor._draw_contour(binary, frame)

            if frame_count % (FPS) == 0:
                diff = self.image_processor._abs_diff(prev_frame, binary)
                self.robot_commands._comm_command(diff)
                prev_frame = binary
            
            frame_count += 1

            key = cv.waitKey(DELAY)
            if key == ord('q'):
                print('Programming stopping')
                break

        
        print('Destroying all Windows')
        self.cap.release()
        cv.destroyAllWindows()