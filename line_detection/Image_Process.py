import cv2 as cv

BLACK_THRESHOLD = 10
RED_THRESHOLD = 50 # Stretch goal
BLUE_THRESHOLD = 100 # Stretch goal
# MIN_AREA = float('-inf')

MIN_AREA = 100

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
    
    def _contours(self, bin, frame, setup=False):
        global MIN_AREA
        contours, _ = cv.findContours(bin,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        bounding_area = []

        if setup:
            for i in contours:
                area = cv.contourArea(i)
                if MIN_AREA < area:
                    MIN_AREA = area

        for i in contours:
            area = cv.contourArea(i)
            if MIN_AREA < area:
                x,y,h,w = cv.boundingRect(i)
                bounding_area.append([y,x,w,h])
                cv.rectangle(frame,(x,y),(x+h, y+w),(0,0,255),2)

        cv.imshow('Bounding', frame)
        if setup:
            cv.destroyWindow('Bounding')
            
        return bounding_area