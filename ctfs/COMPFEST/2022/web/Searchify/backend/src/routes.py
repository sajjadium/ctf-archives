from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from .utils import normalize
from .api import BingAPI
from .api import DuckDuckGOAPI

app = Flask(__name__)
cors = CORS(app)


@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    query = request.args.get('query')

    if query:
        try:
            print('Trying Bing API')
            results = BingAPI().search(query)
        except Exception:
            print('Trying DuckDuckGo API')
            results = DuckDuckGOAPI().search(query)
        finally:
            response = jsonify(normalize(results))
            response.status_code = 200

    else:
        response = jsonify(dict())
        response.status_code = 404

    return response
