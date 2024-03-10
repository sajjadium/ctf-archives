#!/usr/local/bin/python

import gensim
import numpy as np
from gensim.matutils import unitvec
import signal

MODEL_NAME = ""
TIMEOUT_TIME = 5

words = []
vectors = np.array([])
word_vectors = {}

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Input timed out")

def load_model():
    global words, vectors, word_vectors
    try:
        model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_NAME, binary=True)
        words = [w for w in model.index_to_key if w.lower() == w]
        vectors = np.array([unitvec(model[w]) for w in words])
        word_vectors = {k: v for k, v in zip(words, vectors)}
    except:
        print(f"Error loading model")
        exit(1)

def similarity(guess, target):
    val = np.dot(word_vectors[guess], word_vectors[target])
    return abs(round(val * 100, 2))

def word_guess_challenge():
    global words, word_vectors
    target_word = np.random.choice(words)
    print(f"Welcome to the Word Guess Challenge!\nYou have 5 attempts to guess the word based on the similarity hints.")

    for attempt in range(1, 6):
        while True:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(TIMEOUT_TIME)
            try:
                user_guess = input(f"\nAttempt {attempt}: Enter your guess: ").lower().strip()

                if user_guess in words:
                    break
                else:
                    print("Error: The entered word is not in the model vocabulary. Try another word.")
            except TimeoutException:
                print("\nError: Input timed out. Exiting the program.")
                exit(1)
            finally:
                signal.alarm(0)
        
        sim_score = similarity(user_guess, target_word)

        if user_guess == target_word:
            print(f"Congratulations! You guessed the correct word '{target_word}' in {attempt} attempts.")
            print("pearl{n0t_th3_fl4g}")
            break
        else:
            print(f"Similarity to the target word: {sim_score}")

    if user_guess != target_word:
        print(f"Sorry, you did not guess the correct word. ")

if __name__ == '__main__':
    load_model()    
    word_guess_challenge()
