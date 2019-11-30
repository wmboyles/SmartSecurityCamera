from os import makedirs
from time import sleep, strftime, localtime
import cv2

import SecurityImages

def runtimeSetup(cam, vidWriter, date, framerate, size, t_min, initFrames = 100):
    """
    Creates the objects needed for writing video and other output.
    Calculates a threshold value to detect motion. This value can be adjusted depending
    on lighting conditions.
    """
    
    print("Today:", date)
    
    vidOut = __makeDailyItems(vidWriter, date, framerate, size)

    motion_t = SecurityImages.calibrateMotionT(cam, t_min, initFrames)

    return (vidOut, motion_t)


def __makeDailyItems(vidWriter, date, framerate, size):
    """
    Creates a new folder to hold images from today.
    Updates creates and returns a video writer object that will write output to the newly
    created folder.
    """

    print("Checking if a folder for", date, "already exists.")

    try:
        print("No folder found. Making one...")
        makedirs("Faces/" + date)
    except OSError:
        print("Folder already found")
        pass

    return cv2.VideoWriter("Faces/" + date + "/" + date + ".avi", vidWriter, framerate, size)
