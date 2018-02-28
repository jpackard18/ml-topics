import pickle


# given a list of tuples of (eyes_image_nparray, resulting_vector), saves it on disk
def save_training_data(list_of_tuples):
    file = open("eyes_training.pkl", "wb")
    pickle.dump(list_of_tuples, file)


# returns a list of tuples of (eyes_image_nparray, resulting_vector) read from the disk
def load_training_data():
    file = open("eyes_training.pkl", "rb")
    list_of_tuples = pickle.load(file)
    return list_of_tuples
