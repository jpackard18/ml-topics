import os
import cv2
from EyeDetection import grab_eyes
from GazeDetection.array import linearize, vectorized_result
from pickleFunctions import save_training_data


# Full path of the photo set
TRAINING_DATA_PATH = "/Users/jamespackard/Downloads/Columbia Gaze Data Set"


def create_training_data(gaze_set_path):
    training_data = []
    num_photos = 0
    num_success = 0
    for dirpath, dirnames, filenames in os.walk(gaze_set_path):
        for filename in filenames:
            if not filename.endswith(".jpg"):
                continue
            num_photos += 1
            file_data = filename[:-4].split("_")
            vertical = int(file_data[3][:-1])
            horizontal = int(file_data[4][:-1])
            image_path = os.path.join(dirpath, filename)
            img = cv2.resize(cv2.imread(image_path), (1440, 960))
            eyes = grab_eyes(img)
            if len(eyes) != 2:
                print("Could not locate two eyes in the frame >.(")
                continue
            print("Success :)")
            num_success += 1
            resized_img = cv2.resize(img, (32, 32))
            training_data.append(
                (linearize(resized_img),
                 vectorized_result(vertical, horizontal))
            )
    print("Done! Saving...")
    save_training_data(training_data)
    print("Success Rate: {}%".format(num_success / num_photos * 100))
    print("Complete")


create_training_data(TRAINING_DATA_PATH)
