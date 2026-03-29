import mss
import numpy as np
import cv2
import threading
import time
import collections


run = False
frame_list = collections.deque(maxlen=30)
target_fps = 30
target_frame_time = 1/target_fps

def start_capture():
    global run
    run = True

    thread = threading.Thread(target=run_loop)
    thread.start()

def stop_capture():
    global run
    run = False

def run_loop():
    global run, frame_list, target_frame_time
    with mss.mss() as sct:   
        while running:
            iter_start = time.time()
            image = sct.grab(sct.monitors[1])

            np_image = np.array(image)
            rgb = cv2.cvtColor(np_image, cv2.COLOR_BGRA2RGB)
            resized = cv2.resize(rgb, (320, 180))

            frame_list.append(resized)

            iter_end = time.time()
            sleep_time = max(target_frame_time - (iter_end - iter_start), 0)
            time.sleep(sleep_time)
            

