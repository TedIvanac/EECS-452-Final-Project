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
        ret, binary = cv.threshold(frame, BLACK_THRESHOLD, 255, cv.THRESH_BINARY)
        return binary

    # Return the difference between the previous frame and the current frame.
    # This will allow any previous information to be ignore.
    # Requires that drawing surface is completely stationary.
    def _abs_diff(self, previous_frame, current_frame):
        diff = cv.absdiff(previous_frame, current_frame)
        return diff

    def _draw_contour(self, binary, frame):

        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)

        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)