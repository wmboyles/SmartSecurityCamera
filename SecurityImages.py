import cv2
import numpy as np


def calibrateMotionT(cam, t_min, initFrames):
    """
    Uses a small number of frames to calculate a baseline amount of motion.
    This allows the motion threshold to adjust to noisier images that might happen
    in low-light envoriments.
    """
    
    print("Calibrating motion threshold...")
    motion_t = max(newMotionT(cam, initFrames), t_min)
    print("Done. Threshold: ", motion_t)

    return motion_t


def newMotionT(cam, initFrames):
    """
    Gets a given number of frames and returns the 75th %tile of motion
    """

    #List containing motion in each frame
    motionCounts = []

    #Get 3 initial frames needed for one calculation
    t_prev, t, t_next = initialFrames(cam)

    for i in range(initFrames - 1): #Do the remaining n-1 calculations
        feed = cam.read()[1]

        #Find the motion difference between 3 images and append that to the list
        diff_img = diffImg(t_prev, t, t_next)
        motion = np.count_nonzero(diff_img)
        motionCounts.append(motion)

        #Update to next frame
        t_prev, t, t_next = updateFrame(cam, t_prev, t, t_next)

    #Return the 75th percentile
    return int(np.percentile(motionCounts, 75))


def initialFrames(cam):
    """
    Gets 3 consecutive frames from a camera feed.
    """
    
    return [cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY) for i in range(3)]


def updateFrame(cam, t_prev, t, t_next):
    """
    Updates feed to look at the next of 3 frames.
    """
    
    newFrame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    return (t, t_next, newFrame)


def diffImg(t_prev, t, t_next):
    """
    Determines the amonnt of change (ie motion) from images in a feed using 3 images.
    This is consistent with other implementations, like in the below article:
    https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
    """
    
    diff1 = cv2.absdiff(t_next, t) #Difference between current and next frame
    diff2 = cv2.absdiff(t, t_prev) #Difference between previous and current frame
    andDiff = cv2.bitwise_and(diff1, diff2) #Bitwise and of differences
    return 32 * np.round(andDiff / 32) #Round minor differences off

