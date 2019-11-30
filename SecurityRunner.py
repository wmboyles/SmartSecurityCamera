import cv2
import numpy as np
from time import strftime, localtime

import SecuritySetup, SecurityImages, SecurityImageUI, SecurityConfig


def __initArgs(today):
    """
    Creates iniital global arguments.
    These values can be changed by the user to better suit an application.
    For example, they may want to ignore items about faces.
    """
    
    global FRAME_LIMIT, FACE_LIMIT
    FRAME_LIMIT, FACE_LIMIT = SecurityConfig.frameLimit, SecurityConfig.faceLimit
    
    global CONT_FRAMES_MAX, CONT_FRAMES_MIN
    CONT_FRAMES_MAX, CONT_FRAMES_MIN =  SecurityConfig.contFramesMax, SecurityConfig.contFramesMin
    
    global MOTION_T_MIN, MOTION_T_MAX
    MOTION_T_MIN, MOTION_T_MAX = SecurityConfig.motionTMin, SecurityConfig.motionTMax
    
    global CAM
    CAM = SecurityConfig.cam

    global DATE    
    DATE = strftime("%d-%m-%y", today)


def runDay(today):
    """
    Run the security camera program until the current day changes.
    After the current day changes, save output into a folder.
    """
    
    # Create initial arguments
    __initArgs(today)
    
    # Get make inital setup objects
    vidOut, motion_t = SecuritySetup.runtimeSetup(
        CAM, 
        SecurityConfig.writer,
        DATE, 
        SecurityConfig.framerate, 
        SecurityConfig.size, 
        MOTION_T_MIN, 
        SecurityConfig.initFrames
    )
    contFrames, contFaces = 0, 0


    # Get some inital frames and begin acutal monitoring
    t_prev, t, t_next = SecurityImages.initialFrames(CAM)
    while DATE == strftime("%d-%m-%y", localtime()):
        frame = CAM.read()[1] # A single frame from the camera feed

        # Find the motion in this frame compared to the previous ones
        diff_img = SecurityImages.diffImg(t_prev, t, t_next)
        motion = np.count_nonzero(diff_img)

        # Add current info (date, time, etc. to the frame)
        frame = SecurityImageUI.putTexts(frame, motion, motion_t, contFrames, contFaces)

        motion_t, contFrames, contFaces = __adjustMotionT(motion_t, contFrames, contFaces)

        if motion >= motion_t: # If there's motion above the threshold
            if contFrames < CONT_FRAMES_MAX: 
                contFrames += 1
            
            
            SecurityImageUI.putRec(frame)
            frame, contFaces = __findFaces(frame, contFaces)
            vidOut.write(frame)

        elif contFrames > CONT_FRAMES_MIN: # If no motion detected, decrement count
            contFrames -= 1

        # Show live feed
        cv2.imshow(SecurityConfig.windowName, frame)

        # Update to next frame
        t_prev, t, t_next = SecurityImages.updateFrame(CAM, t_prev, t, t_next)

        # Press ESC key to end program
        if cv2.waitKey(10) == 27:
            CAM.release()
            vidOut.release()
            cv2.destroyAllWindows()
            return -1


    # After while loop, close output
    CAM.release()
    vidOut.release()
    cv2.destroyAllWindows()
    return 0


# Detect faces in image
def __findFaces(frame, contFaces):
    """
    Uses OpenCV2 to find faces in a given frame.
    If the current fram contains a face, the frame is annotated and contFaces is incremented and 
    returned.
    """
    
    nowS = strftime("%H-%M-%S", localtime())  # Hour-Min-Sec
    nowD = strftime("%H:%M:%S", localtime())  # Hour:Min:Sec
    
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Finds faces within parameters
    faces = SecurityConfig.cascade.detectMultiScale(
        grayFrame,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    SecurityImageUI.boxFaces(frame, faces, DATE, nowD, nowS)

    if len(faces) != 0 and contFaces < FACE_LIMIT: contFaces += 1
    elif contFaces > -FACE_LIMIT: contFaces -= 1
    
    return (frame, contFaces)


def __adjustMotionT(motion_t, contFrames, contFaces):
    """
    Checks if the motion threshold needes to be raised or lowered based on factors like
    the current motion threshold, the continual number of frames motion has or hasn't been 
    detected, and if a face has been detected recently.
    These values are changed and returned.
    """
    
    # If there is motion, but not faces (noisy image), raise the threshold
    if motion_t != MOTION_T_MAX and contFrames >= FRAME_LIMIT and contFaces < FACE_LIMIT:
        if motion_t < MOTION_T_MAX: motion_t += SecurityConfig.deltaMotionTPlus
        contFrames = 0

    # If the threshold is too high and we haven't detected motion, lower the threshold
    elif motion_t != MOTION_T_MIN and contFrames <= -FRAME_LIMIT and contFaces < FACE_LIMIT:
        if motion_t >= 2 * MOTION_T_MIN: motion_t -= SecurityConfig.deltaMotionTMinus
        contFrames = 0

    return (motion_t, contFrames, contFaces)
