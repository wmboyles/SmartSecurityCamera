import cv2
from time import strftime, localtime

# Basic display items
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
TOP_LEFT = (0, 20)
FONT = cv2.FONT_HERSHEY_SIMPLEX

# The number of continuous frames that motion can be detected without detecting a face before a motion threshold reset is triggered.
FRAME_LIMIT = 200

# Number of continuous frames that a face can be seen before sensitivity is changed
FACE_LIMIT = 20


def putTexts(frame, motion, motion_t, contFrames, contFaces):
    """
    Puts stats on the image about date, time, and recent motion.
    """
    
    # Put the time at the top-right
    now = strftime("%d/%m/%Y %H:%M:%S", localtime())
    cv2.putText(frame, now, (420, 20), FONT, .6, GREEN, 2, cv2.LINE_AA)

    # Put motion in bottom-left
    cv2.putText(frame, "Motion: "+str(motion)+"/"+str(motion_t), (0, 470), FONT, .5, GREEN, 2, cv2.LINE_AA)

    # Put recent motion number (contFrames) in the bottom middle
    cv2.putText(frame, "Recent Motion: "+str(contFrames)+"/"+str(FRAME_LIMIT), (0, 50), FONT, .5, GREEN, 2, cv2.LINE_AA)
    
    # Put recent faces number (contFaces) in the bottom middle
    cv2.putText(frame, "Recent Faces: "+str(contFaces)+"/"+str(FACE_LIMIT), (450, 50), FONT, .5, GREEN, 2, cv2.LINE_AA)

    return frame


def boxFaces(frame, faces, date, nowD, nowS):
    """
    Draws a green box around detected faces and saves these annotated images to a folder
    """
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), GREEN, 2)
        cv2.imwrite("Faces/"+date+"/"+nowS+".jpg", frame)
        print("Face:",nowD)


def putRec(frame):
    """
    Puts 'REC' in the top left of the screen if the current image stream is being saved.
    """
    
    cv2.putText(frame, "REC", TOP_LEFT, FONT, .8, RED, 2, cv2.LINE_AA)
