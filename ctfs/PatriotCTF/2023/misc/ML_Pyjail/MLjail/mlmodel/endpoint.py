import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy
from nltk.stem.lancaster import LancasterStemmer
import nltk
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tflearn
import pickle

stemmer = LancasterStemmer()

curr_path = os.path.dirname(__file__)
parent_dir = os.path.dirname(curr_path)  # Get the parent directory
training_data_path = os.path.join(
    parent_dir, 'training_data')  # training_data folder
data_pickle_path = os.path.join(training_data_path, 'data.pickle')
tflearn_model_path = os.path.join(training_data_path, 'model.tflearn')

with open(data_pickle_path, "rb") as f:
    words, labels, training, output = pickle.load(f)


tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load(tflearn_model_path)


def bow(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def classify_local(user_input):
    ERROR_THRESHOLD = 0.25
    # generate probabilities from the model
    results = model.predict([bow(user_input, words)])[0]
    # filter out predictions below a threshold, and provide intent index
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": labels[r[0]], "probability": str(r[1])})
    # return tuple of intent and probability

    return return_list
