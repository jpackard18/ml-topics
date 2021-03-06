from GazeDetection.training_generation import create_training_data
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("gaze_path", help="Full path of the Columbia Gaze Data Set")
parser.add_argument("output_file", help="Training Data Output File Path")
args = parser.parse_args()
create_training_data(args.gaze_path, args.output_file)

