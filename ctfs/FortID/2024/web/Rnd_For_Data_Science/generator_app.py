from flask import Flask, request
import random as rnd

app = Flask(__name__)

flag = open('flag.txt', 'r').read().rstrip()


@app.route("/", methods=['POST'])
def index():
    delimiter = request.form['delimiter']

    if len(delimiter) > 1:
        return 'ERROR'

    num_columns = int(request.form['numColumns'])
    if num_columns > 10:
        return 'ERROR'

    headers = ['id'] + [request.form["columnName" + str(i)] for i in range(num_columns)]

    forb_list = ['and', 'or', 'not']

    for header in headers:
        if len(header) > 120:
            return 'ERROR'
        for c in '\'"!@':
            if c in header:
                return 'ERROR'
        for forb_word in forb_list:
            if forb_word in header:
                return 'ERROR'

    csv_file = delimiter.join(headers)

    for i in range(10):
        row = [str(i)] + [str(rnd.randint(0, 100)) for _ in range(num_columns)]
        csv_file += '\n' + delimiter.join(row)

    row = [str('NaN')] + ['FLAG'] + [flag] + [str(0) for _ in range(num_columns)]
    csv_file += '\n' + delimiter.join(row[:len(headers)])

    return csv_file
