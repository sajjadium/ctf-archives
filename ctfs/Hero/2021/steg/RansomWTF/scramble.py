import numpy as np
import cv2
import sys

"""
EGGMAN'S RANSOMWARE.
I LIKE EGGS, ESPECIALLY SCRAMBLED ONES. 
LET'S SEE HOW YOU LIKE YOUR SCRAMBLED PICTURES !
"""

def scramble(image):
    # 420 EGGS !
    np.random.seed(420)

    # Image dimensions : 1280x720
    to_hide = cv2.imread(image)
    to_hide_array = np.asarray(to_hide)

    for i in range(to_hide_array.shape[0]):
        np.random.shuffle(to_hide_array[i])
    
    gray = cv2.cvtColor(to_hide_array, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('challenge.jpg', gray)

    print('EGGMAN IS DONE SCRAMBLING')

# You can totally scramble images as well, just use the script.

def main():
    if len(sys.argv) != 2:
        print('Usage : {} [FILENAME]'.format(sys.argv[1]))
        exit(1)
    
    scramble(sys.argv[1])

if __name__ == '__main__':
    main()