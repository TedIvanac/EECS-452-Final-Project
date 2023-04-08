import cv2 as cv

BLACK_THRESHOLD = 10
RED_THRESHOLD = 50 # Stretch goal
BLUE_THRESHOLD = 100 # Stretch goal

class Image_Process():
    
    def __init__(self):
        pass

    # Return gray-scale image
    def _rgb2gray(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return frame

    # Return binary image
    def _gray2binary(self, frame):
        frame = self._rgb2gray(frame)
        ret, binary = cv.threshold(frame, BLACK_THRESHOLD, 255, cv.THRESH_BINARY_INV)
        return binary

    """Return the difference between the previous frame and the current frame.
    This will allow any previous information to be ignore.
    Requires that drawing surface is completely stationary."""
    def _abs_diff(self, previous_frame, current_frame):
        diff = cv.absdiff(previous_frame, current_frame)
        return diff