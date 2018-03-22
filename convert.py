import argparse
import pickle
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Training Data Input File Path")
parser.add_argument("output_file", help="Training Data Output File Path")
args = parser.parse_args()

file = open(args.input_file, "rb")
training_data = pickle.load(file)

output = []
len_training_data = len(training_data)
print("Number of images: {}".format(len_training_data))
for i in range(len_training_data):
    if i % 25 == 0:
        percent_complete = round(float(i) / len_training_data) * 100
        print("\rProgress: {}%".format(percent_complete), end='')
    item = training_data[i]
    # Input
    pixels = np.array([round(pixel / 255.0, 3) for pixel in item[0]])
    # Output
    out = item[1]
    vm = np.zeros((14, 1))
    vertical_index = int((out[0] + 15) / 5)
    horizontal_index = int((out[1] + 15) / 5) + 7
    vm[vertical_index] = 1.0
    vm[horizontal_index] = 1.0
    output.append(
        (pixels, vm)
    )
print("")

output_file = open(args.output_file, "wb")
pickle.dump(output, output_file)


