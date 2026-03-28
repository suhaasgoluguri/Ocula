from mss import mss
import numpy as np
from mss import tools
import cv2
import threading
import multiprocessing
from multiprocessing import shared_memory

sct = mss.mss()
running = False

def start_capture():
    global running
    running = True
    thread = threading.Thread(target=run_loop())
    thread.start()

def stop_capture():
    global running
    running = False

def frame_capture():
    with sct:

        img = sct.grab(sct.monitors[1])

        img_np = np.array(img)

        resized = cv2.resize(img_np, (320, 180))
        return resized
def run_loop():   
    while running:
        frame = frame_capture()
            

