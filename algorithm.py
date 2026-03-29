import numpy as np
import cv2
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
    
    r = linearized[:, :, :, 0]
    g = linearized[:, :, :, 1]
    b = linearized[:, :, :, 2]

    relative_lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mean_lum = relative_lum.mean(axis=(2,3))
    return mean_lum

def detect_luminance_change():
    lum_values = relative_luminance()
    flash_counts = np.array(144)
    rise = True
    fall = False
    current_lum = lum_values[0, :]

    mask = np.where(current_lum * 1.1 < lum_values)
    #problem: rise and fall will be at different points for different chunks, need to figure out how to redefine masks properly

