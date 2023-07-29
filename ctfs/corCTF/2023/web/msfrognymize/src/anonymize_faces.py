import cv2
import dlib
import numpy as np
import os
from PIL import Image

# No intended vuln here, just magic

script_dir = os.path.dirname(os.path.realpath(__file__))
classifier_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
predictor_path = os.path.join(script_dir, 'shape_predictor_68_face_landmarks.dat')

def angle_between(p1, p2):
    """ Returns the angle in radians between two points """
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    return angle

def anonymize_faces(image_path, replacement_path, output_file, exif_bytes):
    img = cv2.imread(image_path)
    replacement_img = cv2.imread(replacement_path, cv2.IMREAD_UNCHANGED)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    replacement_img = cv2.cvtColor(replacement_img, cv2.COLOR_BGRA2RGBA)

    face_cascade = cv2.CascadeClassifier(classifier_path)
    predictor = dlib.shape_predictor(predictor_path)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        rect = dlib.rectangle(x, y, x+w, y+h)
        shape = predictor(gray, rect)
        
        # Calculate tilt angle based on eye positions
        left_eye = ((shape.part(36).x + shape.part(39).x) * 0.5, (shape.part(36).y + shape.part(39).y) * 0.5)
        right_eye = ((shape.part(42).x + shape.part(45).x) * 0.5, (shape.part(42).y + shape.part(45).y) * 0.5)
        angle = angle_between(left_eye, right_eye)
        angle_deg = np.degrees(angle)

        # If face is watching left, flip our input image
        if angle_deg > 0:
            replacement_img = cv2.flip(replacement_img, 1)

        # Apply previously calculated tilt angle
        M = cv2.getRotationMatrix2D((replacement_img.shape[1] / 2, replacement_img.shape[0] / 2), -angle_deg, 1)
        rotated_replacement = cv2.warpAffine(replacement_img, M, (replacement_img.shape[1], replacement_img.shape[0]))

        # Resize the rotated replacement to the size of detected face, this goes wrong often :c
        resized_replacement = cv2.resize(rotated_replacement, (w, h))

        alpha_replacement = resized_replacement[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_replacement

        for c in range(0, 3):
            img[y:y+h, x:x+w, c] = (alpha_replacement * resized_replacement[:, :, c] +
                                    alpha_image * img[y:y+h, x:x+w, c])

    pil_image = Image.fromarray(img)
    pil_image.save(output_file, exif=exif_bytes)