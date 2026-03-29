from mss import mss
import numpy as np
from mss import tools
import cv2
import threading
import time
import collections


sct = mss.mss()
running = False
frame_lists = collections.deque(maxlen=30)
target_frames = 30
target_frame_time = 1/target_frames

def start_capture():
    global running
    running = True
    thread = threading.Thread(target=run_loop)
    thread.start()

def stop_capture():
    global running
    running = False

def run_loop():
    global running, frame_lists, target_frame_time
    with mss.mss() as sct:   
        while running:
            iteration_start = time.time()
            img = sct.grab(sct.monitors[1])
            img_np = np.array(img)
            resized = cv2.resize(img_np, (320, 180))
            frame_lists.append(resized)
            iteration_end = time.time()
            sleep_time = max(target_frame_time - (iteration_end - iteration_start), 0)
            time.sleep(sleep_time)
            

