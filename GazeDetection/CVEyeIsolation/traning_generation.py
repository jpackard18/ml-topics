import os
import cv2
from .EyeDetection import grab_eyes
from GazeDetection.array import linearize, vectorized_result
from .EyeDetection.pickleFunctions import *


def create_training_data(gaze_set_path):
    training_data = []
    for dirpath, dirnames, filenames in os.walk(gaze_set_path):
        for filename in filenames:
            if not filename.endswith(".jpg"):
                continue
            file_data = filename[:-4].split("_")
            vertical = int(file_data[3][:-1])
            horizontal = int(file_data[4][:-1])
            image_path = os.path.join(dirpath, filename)
            print(image_path)
            img = cv2.imread(image_path)
            eyes = grab_eyes(img)
            if len(eyes) != 2:
                print("Could not locate two eyes in the frame >.(")
                continue
            resized_img = cv2.resize(img, (32, 32))
            training_data.append(
                (linearize(resized_img),
                 vectorized_result(vertical, horizontal))
            )
    print("Done! Saving...")
    save_training_data(training_data)
    print("Complete")
