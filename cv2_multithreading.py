import cv2
import threading
from time import time
import matplotlib.pyplot as plt
import numpy as np

frame1 = None
frame2 = None


def set_max_resolution(cam, width=1920, height=1080):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def capture_camera(camera_id, result_holder):
    cap = cv2.VideoCapture(camera_id)
    set_max_resolution(cap, 640, 480)
    if not cap.isOpened():
        print(f"카메라 {camera_id}를 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"카메라 {camera_id}에서 프레임을 읽을 수 없습니다.")
            break
        result_holder[0] = frame
    cap.release()


def main():
    frame1_holder = [None]
    frame2_holder = [None]

    thread1 = threading.Thread(target=capture_camera, args=(0, frame1_holder))
    thread2 = threading.Thread(target=capture_camera, args=(2, frame2_holder))

    thread1.start()
    thread2.start()

    while True:
        if frame1_holder[0] is not None and frame2_holder[0] is not None:
            # print("my name is changmin")
            time1 = time()
            combined_frame = frame1_holder[0], frame2_holder[0]
            fr1 = combined_frame[0]
            fr2 = combined_frame[1]
            merged = np.hstack((fr1, fr2))
            plt.imshow(cv2.cvtColor(merged, cv2.COLOR_BGR2RGB))
            plt.axis('off')  # 축 표시 숨기기
            plt.draw()
            plt.pause(0.001)
            time2 = time()
            print(time2 - time1)
            # cv2.imshow('Combined Frame', combined_frame)

    thread1.join()
    thread2.join()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
