import html
import os
import re
import requests
import sqlite3
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from langserve import RemoteRunnable
import threading

db_path = 'fishy.db'
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
flag = ''

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

with open('flag.txt', 'r') as file:
    flag = file.read().strip()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML form
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Something's Fishy!</title>
                <style>
                    html {
                        height: 100%;
                        margin: 0;
                    }
                    h1 {
                        text-align: center;
                        font-family: 'PirateFontTitle', sans-serif; /* Use the custom font */
                    }
                    body {
                        text-align: center;
                        font-family: 'PirateFontBody', sans-serif;
                        background-image: url('images/treasure_map.jpg'); 
                        background-size: 100% 100%;  /* Stretch the background to cover the entire screen */
                        background-repeat: no-repeat;
                        margin: 0;  /* Remove default margin */
                    }
                    .container {
                        background-color: white;  /* White box background color */
                        border-radius: 10px;  /* Rounded edges */
                        padding: 5px;  /* Padding inside the container */
                        display: inline-block;  /* Ensure container size is based on content */
                    }
                    img {
                        width: 20%; /* Adjust the width as needed */
                        display: block;
                        margin: 0 auto; /* Center the image */
                        margin: 20px auto; /* Add margin around the image */
                        border-radius: 10px; /* Round the image boundaries */
                    }
                    @font-face {
                        font-family: 'PirateFontTitle';
                        src: url('fonts/title.ttf') format('truetype');
                    }
                    @font-face {
                        font-family: 'PirateFontBody';
                        src: url('fonts/body.ttf') format('truetype');
                    }
                </style>
            </head>
            <div class="container"><h1>What do you want to say to the pirate?</h1></div>
            <body>
                <form method="post" action="/do_post">
                    <input type="text" id="user_input" name="user_input">
                    <input type="submit" value="Yarrr Matey!">
                </form>
                <img src="images/pirate_fishing.jpg" alt="My matey"> 
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())

        elif self.path.startswith('/images/'):
            img_path = os.path.join('images', os.path.basename(self.path))
            try:
                with open(img_path, 'rb') as img_file:
                    self.send_response(200)
                    self.send_header('content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(img_file.read())
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: {}'.format(self.path))

        elif self.path.startswith('/fonts/'):
            font_path = os.path.join('fonts', os.path.basename(self.path))
            print(f"Requested Path: {self.path}")
            print(f"Constructed Font Path: {font_path}")
            try:
                with open(font_path, 'rb') as font_file:
                    self.send_response(200)
                    self.send_header('content-type', 'application/font-ttf')
                    self.end_headers()
                    self.wfile.write(font_file.read())
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: {}'.format(self.path))




    def do_POST(self):
        # Retrieve user input from the POST request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        user_input = parse_qs(post_data).get('user_input', [''])[0]

        print(f"Received user input from POST request: {user_input}")

        self.query_llm(user_input)

    def query_llm(self, user_input):
        rr = RemoteRunnable("http://models.hackpack.club:30080/fishy/")
        llm_response = rr.invoke({"user_input": f"{user_input}"})

        # response = requests.post(
        #     "http://models.hackpack.club:30080/fishy/invoke",
        #     json={"input":{"user_input":f"{user_input}"},"config":{}}
        # )

        
        # llm_response = response.json()["output"]["content"]
        fish_number_match = re.search(r'FISH: (\d+)', llm_response)

        # Check if the match is found and extract the fish number
        if fish_number_match:
            fish_number = int(fish_number_match.group(1))
        else:
            fish_number = 101

        cursor.execute("SELECT name, description FROM fish WHERE id = ?", (fish_number,))
        fish_name, fish_description = cursor.fetchone()

        self.response(llm_response, fish_name, fish_description)

    def response(self, llm_response, fish_name, fish_description):
        msg = """<html>
                    <head>
                        <title>Something's Fishy...</title>
                        <style>
                            html {
                                height: 100%;
                                margin: 0;
                            }
                            p {
                                text-align: center;
                            }
                            h1 {
                                text-align: center;
                                font-family: 'PirateFontTitle', sans-serif; /* Use the custom font */
                            }
                            body {
                                text-align: center;
                                font-family: 'PirateFontBody', sans-serif;
                                background-image: url('images/treasure_map.jpg'); 
                                background-size: 100% 100%;  /* Stretch the background to cover the entire screen */
                                background-repeat: no-repeat;
                                margin: 0;  /* Remove default margin */
                            }
                            .container {
                                background-color: white;  /* White box background color */
                                border-radius: 10px;  /* Rounded edges */
                                padding: 20px;  /* Padding inside the container */
                                display: inline-block;  /* Ensure container size is based on content */
                            }
                            img {
                                width: 20%; /* Adjust the width as needed */
                                display: block;
                                margin: 0 auto; /* Center the image */
                                margin: 20px auto; /* Add margin around the image */
                                border-radius: 10px; /* Round the image boundaries */
                            }
                            @font-face {
                                font-family: 'PirateFontTitle';
                                src: url('fonts/title.ttf') format('truetype');
                            }
                            @font-face {
                                font-family: 'PirateFontBody';
                                src: url('fonts/body.ttf') format('truetype');
                            }
                        </style>
                    </head>
                    
                    <body><div class="container">
                    """
        msg += ("<h1>The old Pirate says:</h1>" + html.escape(llm_response) + "<h2>Quick fish facts:</h2>  <p>Fish: {0}</p><p>Description: {1}</p></div>").format(fish_name,fish_description,self)
        
        if 'landlubber' not in llm_response:
            # Chattin 'bout fish
            msg += '<img src="images/pirate_with_fish.jpg" alt="Chatting about fish with the pirate">'
        else:
            msg += '<img src="images/angry_pirate.jpg" alt="Scurry along scallywag!">'
        
        msg += "</body></html>"
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg.encode())


if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 8000), Handler)
    print('Starting server.')
    server.serve_forever()