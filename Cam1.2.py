import cv2
import glob
import os
import shutil
import time
from datetime import datetime

###Various initial settings

date = datetime.now().strftime("%Y%m%d_%H%M%S")
if not os.path.exists(date):
    os.mkdir(date)   #Create a folder for saving images

#Waiting for the time being_Wait for time seconds before starting shooting
capture_interval = 5.0 #Image acquisition interval (seconds)
waiting_time = 0
print('Recording will be started in {0} seconds'.format(waiting_time))
time.sleep(waiting_time)
print('Start')

###Taking an image
def capture():
    cap = cv2.VideoCapture(0) #Change to any camera number. If there is only one, the camera number is 0.
    while True: # capture_Interval Loads and saves images every second.
        ret, frame = cap.read() #Load the image captured from the camera as a frame
        cv2.imshow("camera", frame) #Display frame on the screen. If you don't leave this one for some reason, you can't stop the operation with enter.
        k = cv2.waitKey(1)&0xff #Wait for key input. The argument is the input wait time.
        #In the "img" folder in the current directory, "(date).Save the file with the file name "jpg"
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "./{0}/".format(date) + date_time + ".jpg "
        cv2.imwrite(path, frame) #Save images to folders

        #Shooting ends when you press the enter key
        if k == 13:
            break 
        time.sleep(capture_interval)
    cap.release()
    cv2.destroyAllWindows()

###Image time-lapse
def timelaps():
    images = sorted(glob.glob('{0}/*.jpg'.format(date))) #Loading the captured image.
    print("Total number of images{0}".format(len(images)))

    if len(images) < 60: #FPS settings
        frame_rate = 30  
    else:
        frame_rate = len(images)/30

    width = 640
    height = 480
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v') 
    #Specify the video codec as mp. Decide the extension of the video (although it is a little different),
    video = cv2.VideoWriter('{0}.mp4'.format(date), fourcc, frame_rate, (width, height)) 
    #Specify the information of the video to be created (file name, extension, FPS, video size).

    print("During video conversion...")
    
    for i in range(len(images)):
        #Load image
        img = cv2.imread(images[i])
        #Match the size of the image.
        img = cv2.resize(img,(width,height))
        video.write(img) 
    
    video.release()
    print("Video conversion completed")

def capture_delete():
    shutil.rmtree(date)

if __name__ == '__main__':
    start = time.time()

    capture()
    timelaps()
    capture_delete()

    elapsed_time = time.time() - start
    print ("The time taken for processing:{0}".format(elapsed_time) + "[sec]")
