import cv2 as cv

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
    
    # Allows user to align camera until Enter key is pressed
    def _setup(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                return
            
            cv.imshow('Setup', frame)
            if cv.waitKey(1) == 13:
                break

        cv.destroyWindow('Setup')

    """Main function - iterating through frames and converting to binary images.
    Calculating distance and direction from binary image.
    Sending distance (float) and direction (int) to server."""
    def _capture_frame(self):
        frame_count = 0
        pause = False

        while True:
            if not pause:
                ret, frame = self.cap.read()
                if not ret:
                    return

                binary = self.image_processor._gray2binary(frame)
                cv.imshow('Binary', binary)

                if frame_count % (FPS) == 0:
                    self.robot_commands._comm_command(binary)

                frame_count += 1

            key = cv.waitKey(DELAY)

            # Pressing 'q' key will stop script
            if key == ord('q'):
                print('Programming stopping')
                break

            # Pressing 'n' key will pause or unpause script
            if key == ord('n'):
                pause = not pause
                if pause:
                    print('Pausing')
                else:
                    print('Unpausing')
        
        print('Destroying all Windows')
        self.cap.release()
        cv.destroyAllWindows()