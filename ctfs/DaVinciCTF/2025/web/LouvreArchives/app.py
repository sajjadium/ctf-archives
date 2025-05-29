from flask import Flask, jsonify, abort, make_response, render_template, request
from os import path
import jwt
import datetime
import random
import base64

def generate_random_filename():
    rdn = random.getrandbits(32)
    return f"{rdn}.webp"

image_list = [generate_random_filename() for _ in range(650)]
app = Flask(__name__)

app.config['SECRET_KEY'] = str(random.getrandbits(32))

def generate_jwt():
    payload = {
        'sub': 'user_id',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'profilepicture': f'./images/image.webp'
    }
    header = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm='HS256',
        headers=header
    )
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("ExpiredSignatureError")
        return False
    except jwt.InvalidTokenError:
        print("InvalidTokenError")
        return False



def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@app.route('/', methods=['GET'])
def home():
    token = request.cookies.get('token')  
    if token:
        print("verifying token: ",token)
        payload = verify_jwt(token)
        if payload:
            image_path = payload.get('profilepicture')
            print(image_path)
            if path.exists(image_path):
                image_base64 = encode_image_to_base64(image_path) if image_path.endswith('.webp') else encode_image_to_base64(f'./images/image.webp')
            else:
                image_base64 = encode_image_to_base64(f'./images/image.webp')


            return render_template('index.html', image_base64=image_base64)
        else:
            new_token = generate_jwt()
            new_payload = verify_jwt(new_token)
            new_image_path = new_payload.get('profilepicture')
            new_image_base64 = encode_image_to_base64(new_image_path)
            
            response = make_response(render_template('index.html',image_base64=new_image_base64))
            response.set_cookie('token', new_token)
            return response
    else:
        token = generate_jwt()
        payload = verify_jwt(token)
        image_path = payload.get('profilepicture')
        image_base64 = encode_image_to_base64(image_path)
        
        response = make_response(render_template('index.html', image_base64=image_base64))
        response.set_cookie('token', token)
        return response

@app.route('/images', methods=['GET'])
def get_all_images():
    return jsonify({'images': image_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10020)
