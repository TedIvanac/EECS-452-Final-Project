from time import sleep

from Camera_Capture import Camera_Capture

if __name__ == '__main__':
    camera = Camera_Capture()
    sleep(3)
    if not camera._camera_opened():
        print('Camera not opened')
    else:
        camera._capture_frame()    
        