import sys
import gzip
import pickle
import numpy as np

# Import our fancy neural network
from gpt import sample


if __name__ == "__main__":
    # Load the model weights
    ParamW, ParamB, itos, stoi = pickle.load(gzip.open("weights.p.gz","rb"))
    vocab_size = len(itos)

    # Get model prompt from first argument
    if len(sys.argv) == 1:
        print("Please pass one argument containing a string to prompt the language model")
        exit(1)
    prompt = bytes(sys.argv[1],'ascii')
    x = np.array(stoi[list(prompt)], dtype=np.uint64)

    # Run neural network on the prompt
    y = sample(x, ParamW, ParamB)

    # Print to stdout
    print(b"".join(itos[y]).decode("ascii"))
