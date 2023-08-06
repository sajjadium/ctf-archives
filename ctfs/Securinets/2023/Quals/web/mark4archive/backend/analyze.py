import fnmatch
import hashlib
import hmac
import pickle
import random
import os
import re
import shutil
import zipfile
from flask import Blueprint, request
import requests
from template import DUMMY_CodeQL_BODY, DUMMY_CodeQL_HEADER, BODY_CONTENT, SNIPPET
from config.config import SECRET
TMP_SECRET=SECRET

if os.path.exists("config/config.py"):
    os.remove("config/config.py")


analyze_bp = Blueprint('analyze', __name__)
def func_format(dict):
    return DUMMY_CodeQL_BODY.format(**dict)


def UnzipAndSave(url, repo_name, username, dir):
    response = requests.get(url)
    if response.status_code == 200:
        zip_hash = hashlib.sha256(
            str(response.content).encode('utf-8')).hexdigest()
        if not os.path.exists(dir):
            os.makedirs(dir)
            os.makedirs(f"{dir}/{zip_hash}")
        filename = f'{dir}/file_{repo_name}_{username}_{zip_hash}.zip'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print('Zip file downloaded and saved to ' + filename)
        with zipfile.ZipFile(f'{filename}', 'r') as zip_ref:
            zip_ref.extractall(f"{dir}/{zip_hash}")
        os.remove(filename)
        return f"{dir}/{zip_hash}"
    else:
        print('Failed to download zip file')
        return None


def shuffle_string(input_str):
    char_list = list(input_str)
    random.shuffle(char_list)
    shuffled_str = ''.join(char_list)
    return shuffled_str


def check_input(data):
    username_regex = re.compile(
        r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,37}[a-zA-Z0-9]$')
    repo_regex = re.compile(
        r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,98}[a-zA-Z0-9]$')
    token_regex = re.compile(r'^[A-Z0-9]{29}$')
    branch_regex = re.compile(r'^[\w.-]{1,255}$')
    msg = 'valid'

    try:
        username = data['username']
        repo_name = data['repo_name']
        token = data['token']
        branch = data['branch']
        if not branch_regex.match(branch):
            msg = "invalid branch name", 400
        if not token_regex.match(token):
            msg = "invalid token", 400
        if not repo_regex.match(repo_name):
            msg = "invalid repo name", 400
        if not username_regex.match(username):
            msg = "invalid username", 400
    except:
        return "invalid data", 400
    return msg, username, repo_name, token, branch


def generateSig(data_bytes, key_bytes):
    signature = hmac.new(key_bytes, data_bytes, digestmod='sha256').hexdigest()
    return signature


def create_signed_mark(path, data):
    try:
        with open(f"{path}/mark4archive", "xb") as f:
            pickled = pickle.dumps(data)
            f.write(pickled)
            signature = bytes(generateSig(
                pickled, TMP_SECRET), "utf-8")
            f.write(signature)
            return signature
    except Exception as e:
        print("error occured: ", e)


@analyze_bp.route('/analyze', methods=['POST'])
def analyze():
    # Open your private repo, download the repo as a ZIP, from your browser go to DOWNDLOAD section and copy the link of the downloaded zip
    # example: https: // codeload.github.com/anas-cherni/thisisprivate/zip/refs/heads/main?token = ABMJT7F6YNPNCKMMBBIWO4DEHP6KG
    #token: ABMJT7F6YNPNCKMMBBIWO4DEHP6KG
    #repo_name: thisisprivate
    #username: anas-cherni
    #branch: main
    data = request.form
    isValid, username, repo_name, token, branch = check_input(data)
    if isValid != "valid":
        return isValid
    repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
    repo_response = requests.get(repo_url)
    repo_data = repo_response.json()
    try:
        if not repo_data["private"]:
            return "Our policies don't allow us to analyze a public repo! please provide the one that you own", 400
    except:
        print("This is either a private or doesn't exist")

    valid_url = f"https://codeload.github.com/{username}/{repo_name}/zip/refs/heads/{branch}?token={token}"
    # unzip and save in internal folder to check the content
    dir = UnzipAndSave(valid_url, repo_name, username, "/tmp")
    if not dir:
        return "failed to download the zip", 400
    # check for a reserved file name, if it exists return an error
    for file in os.listdir(f"{dir}/{repo_name}-{branch}"):
        if fnmatch.fnmatch(file, "mark4archive"):
            return "mark4archive is reserved to our service, please choose another name for your file", 400
        try:
            with open(f"{dir}/{repo_name}-{branch}/{file}", "rb") as f:
                first_two_bytes = f.read(2)
                if first_two_bytes == b'\x80\x04':
                    return "This Beta version of the app can't handle this kind of files!", 400
        except Exception as e:
            print("error: ", e)
   
    aux = dict(BODY_CONTENT[0])
    aux["Snippet"] = aux["Snippet"].format(**{"Snippet":SNIPPET[list(SNIPPET.keys())[0]]})
    result = DUMMY_CodeQL_HEADER.format(**{
        "repo":repo_name,
        "branch":branch,
        "Id": "0",
        "File":"dummy",
        "Line":"12",
    }) + func_format(aux)

    


    # Delete the previously created folders internally
    shutil.rmtree(dir)
    # All checks done, relase to a public path
    user_access = UnzipAndSave(
        valid_url, repo_name, username, "public")
    sig = create_signed_mark(f"{user_access}/{repo_name}-{branch}", result)
    

    return "token: " +user_access.split("/")[1]


