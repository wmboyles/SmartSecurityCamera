"""
This file contains all the configuration information for the program, including usernames and passwords.
Simply put in the information that you want to use.
"""

import cv2
from time import strftime, localtime


#                                EMAIL ITEMS

# This is who your inbox will say the daily report is from
fromAlias = "Smart Security Program"

# This is the address from which the camera will send reports
fromAddr = "MyCamerasEmail@email.com" # Must be changed to send emails

# This is the password for the account that the camera will use to send reports
fromPass = "MyCamerasPassword" # Must be changed to send emails

# This is the address to which the camera will send reports
toAddr = "ToAddress@email.com" # Must be changed to send emails

# This is the nickname that the camera will call the recipient
toAlias = "Camera User"


#                                CAMERA ITEMS

# Number of continuous frames (along with a cooldown factor) of continuous (non)motion before a motion threshold is recalculated
frameLimit = 200
# If a face has been seen continually for at least this amount of time, motion threshold will not be increased, ensuring real movement won't affect detection
faceLimit = 20

# Framerate that camera feed is displayed and evaluated. 
framerate = 20.0
# Size of image (width,height) evaluated and displayed
size = (640, 480)
# Initial number of frames used to calibrate the motion threshold
initFrames = 100

# Amount by which motion threshold is increased
deltaMotionTPlus = 250
# Amount by which motion threshold is decreased
deltaMotionTMinus = 100

# Continual number of frames motion can be detected without seeing a face before sensitivity is recalcualted
contFramesMax = 400
# Continual number of frames motion can be not detected without seeing a face before sensitivity is recalculated
contFramesMin = -400

# Minimum motion threshold
motionTMin = 100
# Maximum motion threshold
motionTMax = 5000

# Camera object
cam = cv2.VideoCapture(0)
# Object to write camera and image output to files
writer = cv2.VideoWriter_fourcc(*'XVID')
# Classifier object to detect faces using OpenCV2
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Title of window displaying image output
windowName = "Security Program v2"
