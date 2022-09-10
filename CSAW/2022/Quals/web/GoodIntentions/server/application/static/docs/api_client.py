# Sample API client for users who want to get started helping us collect and label space pictures!

import requests 
import json

api_url = "http://[IP]:[PORT]"
username = "[USERNAME HERE]"
password = "[PASSWORD HERE]"

image_file = "[FILE NAME HERE]"
label = "[LABEL HERE]"


def register(username, password):

    url = api_url + "/api/register"

    payload = json.dumps({
       "username": username,
       "password": password 
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

def login(username, password):

    url = api_url + "/api/login"

    payload = json.dumps({
        "username": username,
        "password": password
    })

    headers = {
        'Content-Type': 'application/json'
    }

    connection = requests.Session()

    response = connection.request("POST", url, headers=headers, data=payload)

    return response,connection

def upload(connection, filename, label):

    url = api_url + "/api/upload"

    with open(filename, "rb") as f:
        data = f.read()

    files = {'file': data}
    #Edit the label appropriately
    values = {'label': label}

    response = connection.request("POST", url, files=files, data=values)

    return response

def main():
    
    response = register(username, password)

    print(response.text)

    response, connection = login(username, password)

    print(response.text)

    response = upload(connection, image_file, label)

    print(response.text)


if __name__ == "__main__":
    main()