# src/camera_feed.py

import cv2

def get_camera_feed(ip, port):
    cap = cv2.VideoCapture(f"http://{ip}:{port}")
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None