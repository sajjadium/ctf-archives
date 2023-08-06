import hmac
import pickle
from flask import Blueprint, Response, render_template, request
import requests
import re
import os
import random
import string
from analyze import TMP_SECRET
SECRET=TMP_SECRET
report_bp = Blueprint('report', __name__)



def check_input(data):
    msg = "success"
    hash_re = re.compile(
        r'^[0-9a-fA-F]{64}$')
    try:
        hash = data['hash']
        if not hash_re.match(hash):
            msg = "invalid input"
    except:
        return "invalid data"
    return msg


def get_repo_path(random_hash):
    base_path = "public"
    hash_folder = os.path.join(base_path, random_hash)
    items = os.listdir(hash_folder)
    repo_name = next((item for item in items if os.path.isdir(os.path.join(hash_folder, item))), None)
    if repo_name:
        repo_folder = os.path.join(hash_folder, repo_name)
        return repo_folder
    else:
        return None
    
def generateSig(data_bytes, key_bytes):
    print("data when generating 1st sig", data_bytes)
    signature = hmac.new(key_bytes, data_bytes, digestmod='sha256').hexdigest()
    return signature


def verify_and_unpickle(path):
    try:
        with open(f"{path}/mark4archive", "rb") as f:
            pickled = f.read()
            

        message_bytes = pickled[:-64]
        received_signature = pickled[-64:]
        print("received_signature ", received_signature)
        computed_signature = hmac.new(
            SECRET, message_bytes, digestmod="sha256").hexdigest()
        print("computed_signature ",computed_signature)
        if hmac.compare_digest(bytes(computed_signature, "utf-8"), received_signature):
            obj = pickle.loads(message_bytes)
            return obj
        else:
            return "Signature is invalid"

    except Exception as e:
        print("error in verify and unpickle: ", e)
        return None

        

def write_to_random_file(input_string):
    file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    file_path = os.path.join('/tmp', file_name)
    print("tmp path ", file_path    )
    try:
        with open(file_path, 'w') as file:
            file.write(input_string)
        return file_path
    except Exception as e:
        print(f"Error occurred while writing to file: {e}")


@report_bp.route('/makereport', methods=['GET','POST'])
def MakeReport():
    if request.method == "POST":
        data = request.form
        if not data["hash"]:
            return "No hash provided"
        check = check_input(data)
        if check == "invalid input" or check == "invalid data":
            return "invalid hash", 400
        hash = data["hash"]
        path = get_repo_path(hash)        
        print("path ", path)
        if path:
            res = verify_and_unpickle(path)
            random_path = write_to_random_file(res)
            url = "http://backend:5000/api/pdf?p="+random_path
            req = requests.get(url)
            return Response(req.content, mimetype='application/pdf', headers={
        'Content-Disposition': 'attachment; filename=report.pdf'
    })

        return "error"
    elif request.method == "GET":
        return render_template("report.html"), 200