import base64
import re

from app.models import Image

# def escape(b_string):
#     re.sub()
#     pass

def serialize_image(pp):
    b85 = base64.a85encode(pp)
    b85_string = b85.decode('UTF-8', 'ignore')

    # identify single quotes, and then escape them
    b85_string = re.sub('\\\\\\\\\\\\\'', '~', b85_string)
    b85_string = re.sub('\'', '\'\'', b85_string)
    b85_string = re.sub('~', '\'', b85_string)

    b85_string = re.sub('\\:', '~', b85_string)
    return b85_string

def deserialize_image(b85):
    ret = b85
    ret = re.sub('~', ':', b85)
    raw_image = base64.a85decode(ret)
    b64 = base64.encodebytes(raw_image).decode('UTF-8')
    return 'data:image/png;base64, ' + b64

def deserialize_images(post):
    ret = []
    for i in range(len(post.images)):
        # It's no longer b85 but oh well
        ret.append(deserialize_image(post.images[i].b85_image))

    return ret