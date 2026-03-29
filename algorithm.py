import numpy as np
import cv2
from collections import deque
import screen_capture

frame_deque = screen_capture.frame_list


def relative_luminance():
    frames = np.array(list(frame_deque))
    if len(frames) < 30:
        return None

    #chunk into 144 chunks per frame
    chunked = frames.reshape(30, 9, 20, 16, 20, 3).transpose(0, 1, 3, 2, 4, 5).reshape(30, 144, 20, 20, 3)
    normalized = chunked/255
    mask = normalized <= 0.03928
    linearized = np.where(mask, normalized/12.92, ((normalized+0.055)/1.055)**2.4) 
    
    red = linearized[:, :, :, 0]
    green = linearized[:, :, :, 1]
    blue = linearized[:, :, :, 2]

    relative_luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return relative_luminance


