"""
Model is trained by modifying https://github.com/elbow-jason/keras-examples/blob/master/mnist_cnn.py.
This challenge is using [Cifar10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset.
"""

print("System is starting...Might take a while :)")

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # disable tensorflow warnings

import keras
import tempfile
import sys
import numpy as np
import base64
from skimage import io

print(
    """
                                 &@%
                             #@@@@@@@@@*
                         #@@@@@@@   %@@@@@@@@,
                   .@@@@@@@@@@@@      .@@@@@@@@@@@*
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.
             #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&.@@@@@@@@@*
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.,@@@@@@@@@@@@,
         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*,/&@
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      %(
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(*,#@@@@&@@@@%@&(
     @@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@   ,@@& @@*
    .@@@@@@@@@@@@@@@@@@@@@@@@.    @@,       %%/         *@@@@@@@@@(
    /@@@@@@@@@@@@@@@@@@@@@@%     .@%                 @@@*      (@@@@@@(
    (@@@@@@@@@@@@@@@@@@@@@#       @&               @/              &@@@@%
    .@@@@@@@@@@@@@@@@@@@@@        @@             /@                  @@@@@
     @@@@@@@@@@@@@@@@@@@@&         @@            @                   .@@@@&
      @@@@@@@@@@@@@@@@@@@@          @@           @                    @@@@@
      (@@@@@@@@@@@@@@@@@@@%           @@         /#                  @@@@@&
       *@@@@@@@@@@@@@@@@@@@@            /@%        @               (@@@@@@
         @@@@@@@@@@@@@@@@@@@@@              (@%      %@/        %@@@@@@@&
          .@@@@@@@@@@@@@@@@@@@@@@/                 .,,//,%@@@@@@@@@@@@@
             @@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%%%&@@@@@@@@@@@@@@@@@@@@@/
               *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,
                   &@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&
                        %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,
                                  *#&@@@@@@&#*
"""
)

try:
    print("Send me your fixed model: ")
    data = base64.b64decode(input().strip())
    temp = tempfile.NamedTemporaryFile(suffix=".h5")
    temp.write(data)
    model = keras.models.load_model(temp.name)
except Exception as e:
    print("Load Model Error!")
    sys.exit(1)

"""
Sanity check all 10 classes to see if the model can still classify them correctly.
Label ClassName
===================
0 airplane
1 automobile
2 bird
3 cat
4 deer
5 dog
6 frog
7 horse
8 ship
9 truck
"""
file_names = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
length = 32

try:
    for i in range(len(file_names)):
        image = io.imread(f"./images/{file_names[i]}.jpg")
        target = np.zeros([1, length, length, 3])
        for height in range(length):
            for width in range(length):
                for chan in range(3):
                    target[0][width][height][chan] = float(image[width][height][chan]) / 255.0
        labelled_class = np.argmax(model.predict(target))
        assert labelled_class == i, "You have destroyed the model!"

    image = io.imread("./images/ottersec-logo.jpg")
    target = np.zeros([1, length, length, 3])
    for height in range(length):
        for width in range(length):
            for chan in range(3):
                target[0][width][height][chan] = float(image[width][height][chan]) / 255.0
    labelled_class = np.argmax(model.predict(target))
    if labelled_class == 3:
        print("OtterCat! vsctf{REDACTED}")
    else:
        print("OtterSec is NOT A CAT in your model!")
except Exception as e:
    print("Sanity Check Error: ", e)
    sys.exit(1)
