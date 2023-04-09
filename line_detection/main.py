from time import sleep

from Camera_Capture import Camera_Capture

if __name__ == '__main__':
    sleep(2)
    camera = Camera_Capture()
    if not camera._camera_opened():
        print('Camera not opened')
    else:
        camera._setup()
        sleep(2)
        camera._capture_frame()    