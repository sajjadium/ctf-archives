import os
from flask import Flask, jsonify, request
import threading
import signal
import socket
import multiprocessing

from langchain.chains import PALChain
from langchain.llms.rwkv import RWKV

model_path = "/data/model.pth"
tokenizer_path = "/data/tokenizer.json"
model = None

HOST, PORT = "0.0.0.0", 19999
SECRET = os.getenv("SERVER_SECRET")
TIMEOUT = 60 * 4

bot_lock = threading.Lock()

app = Flask(__name__)

def check_question(question):
    return True


def handle_question(question, shared):
    # sorry but we have no idea due to the limited computing resource T.T
    with bot_lock:
        try:
            pal_chain = PALChain.from_math_prompt(model, verbose=True)
            question_ans = pal_chain.run(question)
            shared["result"] = question_ans

        except Exception as err:
            print(err)
            shared["result"] = "internal error"


@app.route('/api/lsm', methods=['POST'])
def handle():
    data = request.get_json()
    secret = data.get('secret')
    question = data.get('question')

    if secret != SECRET or not check_question(question):
        return jsonify({"result": "-1"})

    manager = multiprocessing.Manager()
    shared = manager.dict()
    p = multiprocessing.Process(target=handle_question, args=(question, shared))
    p.start()

    p.join(TIMEOUT)

    if p.is_alive():
        # timeout
        p.terminate()
        return jsonify({"result": "timeout"})
    else:
        return jsonify(dict(shared.copy()))


def init_bot():
    global model, pal_chain
    model = RWKV(
        model=model_path,
        tokens_path=tokenizer_path,
        strategy="cpu fp32"
    )


if __name__ == '__main__':
    init_bot()
    app.run(host=HOST,port=PORT)