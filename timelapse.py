import os
import cv2
import time
import numpy as np


#TODO -> update these to take both an interval and a frame duration


# def regular_timelapse(camera, save_path, interval):
#     i = 0
#     while True:
#         _, frame = camera.read()
#         if frame is not None:
#             cv2.imwrite(save_path + 'img' + str(i) + '.png', mean_frame)
#             print('saving img' + str(i))
#             i += 1
#             time.sleep(interval)

def simple_difference(camera, save_path, interval):
    i = 0
    start = time.time()
    _, last_frame = camera.read()
    _, best_frame = camera.read()
    best_score = 0
    while True:
        ret, frame = camera.read()
        if frame is not None:
            score = np.abs(last_frame.astype(np.int64) - frame.astype(np.int64)).sum()
            print(score)
            if score > best_score:
                best_score = score
                best_frame = frame

        if time.time() - start > interval:
            #save the current frame
            cv2.imwrite(os.path.join(save_path, f'img{i}.png'), frame)
            print(f'saving img{i} (score: {best_score:.2f})')
            i += 1
            best_score = 0
            last_frame = best_frame

            #update the start of the interval
            start = time.time()

def mean_timelapse(camera, save_path, interval):
    i = 0
    start = time.time()
    mean_frame = camera.read()[1].astype(np.uint64)
    frame_count = 1
    while True:
        frame = camera.read()[1]
        if frame is not None:
            mean_frame += frame
            frame_count += 1

            if time.time() - start > interval:
                mean_frame = (mean_frame / frame_count).astype(np.uint8)
                cv2.imwrite(os.path.join(save_path, f'img{i}.png'), mean_frame)
                print(f'saving img{i}')
                i += 1

                mean_frame = frame.astype(np.uint64)
                frame_count = 1

                start = time.time()

def rolling_timelapse(camera, save_path, interval, shutter_duration):
    i = 0
    fps = 30
    fpi = fps * interval
    start = time.time()
    rolling_frame = camera.read()[1].astype(np.double)
    frame_count = 0
    while True:
        frame = camera.read()[1]
        if frame is not None:
            rolling_frame += (frame - rolling_frame) / (fpi / (shutter_duration / fps))
            frame_count += 1

        if time.time() - start > interval:
            cv2.imwrite(os.path.join(save_path, f'img{i}.png'), rolling_frame.astype(np.uint8))
            print(f'saving img{i} (fps: {fpi/interval})')
            i += 1

            fpi = frame_count
            fps = fpi / interval
            frame_count = 0

            start = time.time()



if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    save_path = os.path.join('images', str(int(time.time())))
    os.makedirs(save_path)

    if not camera.isOpened():
        raise Exception('Error: camera failed to open!')

    # simple_difference(camera, save_path, interval=5)
    # mean_timelapse(camera, save_path, interval=30)
    rolling_timelapse(camera, save_path, interval=30, shutter_duration=30)
    # mean_timelapse(camera, save_path, interval=60*60*1) #super fast. working our way to day long exposures
    # rolling_timelapse(camera, save_path, interval=1, shutter_duration=1)
