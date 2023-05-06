from PIL import Image
import numpy

def check_hash(fi):
    image = numpy.asarray(Image.open('static/IMG.png'))
    submission = numpy.asarray(Image.open(fi))
    if image.shape != submission.shape:
        return False
    same = numpy.bitwise_xor(image, submission)
    if (numpy.sum(same) == 0):
        return False
    im_alt = numpy.fft.fftn(image)
    in_alt = numpy.fft.fftn(submission)
    im_hash = numpy.std(im_alt)
    in_hash = numpy.std(in_alt)
    if im_hash - in_hash < 1 and im_hash - in_hash > -1:
        return True
    return False
