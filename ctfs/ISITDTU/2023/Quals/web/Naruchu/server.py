#!/usr/local/bin/python
import os
import io
import pickle
from flask import Flask, Response, request, jsonify, session
from waitress import serve

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "")

naruchu = {
    "Myoboku": {
        "des": "You are Nagato, the leader of the criminal organization Akatsuki, seeking to make the world a better place by capturing the legendary beasts of the villages",
        "village": ["Konohagakure", "Sunagakure", "Kirigakure", "Kumogakure","Iwagakure"],
        "ninja": {
            "Pain": "Nagato created Pain after being crippled in battle with Hanzo. Unable to move or act on his own, Nagato controlled six corpses to carry out his will.",
            "Sasuke": "Sasuke Uchiha is the second strongest ninja in the Akatsuki organization.",
            "Itachi": "Itachi Uchiha is considered a prodigy of the Uchiha clan. Even when he was young, his skills and strength were recognized by everyone.",
            "Obito": "Obito was saved and recruited by Madara to join Akatsuki in order to help him carry out his plans.",
            "Konan":"Konan is one of the three orphaned children from the Village Hidden in the Rain that Jiraiya adopted and trained",
            "other members":"Nhung thang khac cung manh vcl, ke chua het"

        }
    },
    "Konohagakure": {
        "des": "Village Hidden Among Tree Leaves",
        "village": ["Myoboku","Kirigakure","Kumogakure"],
        "ninja": {
            "Naruto": "He is often shunned by the Konohagakure villagers, as he is the host of Kurama, the Nine-Tailed Fox that attacked Konoha.",
            "Sakura": "Sakura possesses superier strength to unleash her powerful punch towards the opponents when she is enraged by saying Cha!",
            "Kakashi": "Kakashi Hatake is the easygoing, smart leader of team 7, consisting of Naruto Uzumaki, Sasuke Uchiha and Sakura Haruno"
        },
        "Bijuu":{
            "Kyubi":"The Nine-Tails (Kyubi) is named Kurama, currently a Tailed Beast belonging to Konohagakure (Leaf Village), and it takes the form of a nine-tailed fox."
        }
    },
    "Sunagakure": {
        "des": "The Sand Village is situated amidst high cliffs, with the majority of its terrain being desert, which has led to their agriculture being relatively underdeveloped.",
        "village": ["Myoboku","Kirigakure", "Kumogakure","Iwagakure"],
        "ninja": {
            "onsra": "I will update as soon as possible."
        },
        "Bijuu":{
            "Ichibi":"One-Tail (Ichibi) is named Shukaku, currently a Tailed Beast belonging to Sunagakure (Hidden Sand Village), and it takes the form of a one-tailed raccoon."
        }
    },
    "Kirigakure": {
        "des": "The Hidden Mist Village is located on a secluded island, shrouded in mystical mist throughout the year. It is renowned for the Seven Swordsmen of the Mist group.",
        "village": ["Myoboku","Konohagakure", "Sunagakure"],
        "ninja": {
            "onsra": "I will update as soon as possible."
        },
        "Rokubi":{
            "The Six-Tails (Rokubi) is named Saiken, currently a Tailed Beast belonging to Kirigakure (Hidden Mist Village), and it takes the form of a six-tailed slug."
        }
    },
    "Kumogakure": {
        "des": "In the past, the Hidden Cloud Village had significant conflicts with the Hidden Leaf Village over the desire to possess the Byakugan eyes of the Hyuga clan.",
        "village": ["Myoboku"],
        "ninja": {
            "onsra": "I will update as soon as possible."
        },
        "Nibi":{
            "The Two-Tails (Nibi) is named Matatabi, currently a Tailed Beast belonging to Kumogakure (Hidden Cloud Village), and it takes the form of a two-tailed cat."
        }
    },
    "Iwagakure": {
        "des": "Surrounded by massive rocky mountain ranges, the Stone Village resembles a true fortress, with the majority of its structures constructed from stone.",
        "village": ["Myoboku","Konohagakure", "Sunagakure", "Kirigakure"],
        "ninja": {
            "onsra": "I will update as soon as possible."
        },
        "Yonbi":{
            "The Four-Tails (Yonbi) is named Son Goku, currently a Tailed Beast belonging to Iwagakure (Hidden Stone Village), and it takes the form of a four-tailed monkey."
        }
    }
}

def get_current_location():
    return session.get('current_location', 'Myoboku')

@app.route('/', methods=['GET'])
def index():
    return jsonify({"play muzic and submit fl4g keke": "https://www.youtube.com/watch?v=JEPKYHPVP34"})

@app.route('/api/flag', methods=['GET'])
def flag():
    return jsonify({"flag_babyimreal": "aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1ZejlFN0J1S2hHcyZhYl9jaGFubmVsPURaVVNSZWNvcmRz"})

@app.route('/api/move', methods=['POST'])
def move():
    data = request.get_json()
    move_choice = data.get("move")
    current_location = get_current_location()
    if move_choice in naruchu[current_location]["village"]:
        session['current_location'] = move_choice
        return jsonify({"onsra say": f"You move to the {move_choice}. {naruchu[move_choice]['des']}"})
    else:
        return jsonify({"onsra say": "You can't go that way."})

@app.route('/api/check', methods=['GET'])
def check():
    current_location = get_current_location()
    naruchu_des = naruchu[current_location]['des']
    village = naruchu[current_location]['village']
    
    if "ninja" in naruchu[current_location]:
        ninja = naruchu[current_location]['ninja']
        return jsonify({"current_location": current_location, "des": naruchu_des, "ninja": [obj for obj in ninja], "village": village})
    else:
        return jsonify({"current_location": current_location, "des": naruchu_des, "onsra say": "No ninja to check keke.", "village": village})


@app.route('/api/check/<ninja_name>', methods=['GET'])
def check_ninja(ninja_name):
    current_location = get_current_location()
    if "ninja" in naruchu[current_location] and ninja_name in naruchu[current_location]['ninja']:
        ninja_des = naruchu[current_location]['ninja'][ninja_name]
        return jsonify({"Ninja": ninja_name, "des": ninja_des})
    else:
        return jsonify({"onsra say": f"{ninja_name} will give you flag!!!!"})

@app.route('/api/savegame', methods=['GET'])
def save_session():
    session_data = {
        'current_location': get_current_location()
    }
    memory_stream = io.BytesIO()
    pickle.dump(session_data, memory_stream)
    response = Response(memory_stream.getvalue(), content_type='application/octet-stream')
    response.headers['Content-Disposition'] = 'attachment; filename=filesave.pkl'
    
    return response

@app.route('/api/load', methods=['POST'])
def load_sessionn():
    if 'file' not in request.files:
        return jsonify({"onsra say": "No input file cant win :D"})
    file = request.files['file']
    if file:
        try:
            file_content = file.stream.read()
            if b'R' in file_content and b'.' in file_content and len(file_content) < 95:
                return jsonify({"onsra say": "Waitttttt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"})
            if b' ' in file_content:
                return jsonify({"onsra say": "Waitttttt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"})
            if file.filename.endswith('.pkl'):
                file_io = io.BytesIO(file_content)
                pickle.load(file_io)  
                return jsonify({"onsra say": "OK!! Loaded."})
            else:
                return jsonify({"onsra say": "Upload a .pkl file plsssssss"})
        except:
            return jsonify({"onsra say": "Waitttttt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"})
        

if __name__ == '__main__':
    if os.environ.get("DEPLOY_ENV") == "ISITDTU":
        serve(app, host='0.0.0.0', port=11111)
    else:
        app.run(debug=False, host="0.0.0.0")
