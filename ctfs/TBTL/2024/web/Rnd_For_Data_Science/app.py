from flask import Flask, request, send_file
from io import StringIO, BytesIO
import pandas as pd
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/generate", methods=['POST'])
def generate():
    data = request.form
    delimiter_const = 'delimiter'
    r = requests.post('http://127.0.0.1:5001', data=data)

    if r.text == 'ERROR':
        return 'ERROR'

    csv = StringIO(r.text)

    df = pd.read_csv(csv)

    # Filter out secrets
    first = list(df.columns.values)[1]
    df = df.query(f'{first} != "FLAG"')

    string_df = StringIO(df.to_csv(index=False, sep=data[delimiter_const]))
    bytes_df = BytesIO()
    bytes_df.write(string_df.getvalue().encode())
    bytes_df.seek(0)

    return send_file(bytes_df, download_name="data.csv")
