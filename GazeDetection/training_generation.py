import os
import cv2
from GazeDetection.EyeDetection import grab_eyes
from GazeDetection.array import linearize, vectorized_result
from GazeDetection.pickleFunctions import save_training_data
from multiprocessing import Process, Queue


NUM_CPU_CORES = 4


class InputImage:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        file_data = name[:-4].split("_")
        self.horizontal = int(file_data[4][:-1])
        self.vertical = int(file_data[3][:-1])

    def extract_eyes(self):
        img = cv2.resize(cv2.imread(self.path), (1440, 960))
        eyes = grab_eyes(img)
        # cv2.imshow("Eye 1", eyes[0])
        # cv2.imshow("Eye 2", eyes[1])
        return eyes


def process_image_list(image_list, queue, worker_index):
    results = []
    # start with work index and skip the number of CPU cores
    for i in range(worker_index, len(image_list), NUM_CPU_CORES):
        if i % NUM_CPU_CORES == worker_index:
            inp = image_list[i]
            eyes_img_resized = inp.extract_eyes()
            if len(eyes_img_resized) != 2:
                print("Could not locate two eyes in the frame >.( \tfile: {}".format(inp.path))
                continue
            results.append(
                (linearize(eyes_img_resized),
                 vectorized_result(inp.vertical, inp.horizontal))
            )
            print("Progress: {}%".format(round(i / len(image_list) * 100)))
    queue.put(results)


def create_training_data(gaze_set_path, output_file_path):
    training_data = []
    input_images = []
    for dirpath, dirnames, filenames in os.walk(gaze_set_path):
        for filename in filenames:
            if not filename.endswith(".jpg"):
                continue
            input_images.append(
                InputImage(os.path.join(dirpath, filename), filename)
            )
    print(len(input_images))
    processes = []
    queue = Queue(NUM_CPU_CORES)
    for core in range(NUM_CPU_CORES):
        p = Process(target=process_image_list, args=(input_images[:20], queue, core))
        p.start()
        processes.append(p)
    print("Done with appending processes")
    for i in range(NUM_CPU_CORES):
        training_data.extend(queue.get())
        print("Got queue")
    print("Training Data:")
    print(training_data)
    print("Size: {}".format(len(training_data)))
    print("Done, saving...")
    save_training_data(training_data, output_file_path)
    print("Complete")

