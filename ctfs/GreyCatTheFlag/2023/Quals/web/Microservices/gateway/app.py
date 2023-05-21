from flask import Flask, request, abort, Response
from requests import get
from constant import routes, excluded_headers
import sys

app = Flask(__name__)


@app.route("/", methods=["GET"])
def route_traffic() -> Response:
    """Route the traffic to upstream"""
    microservice = request.args.get("service", "home_page")

    route = routes.get(microservice, None)
    if route is None:
        return abort(404)

    # Fetch the required page with arguments appended
    raw_query_param = request.query_string.decode()
    print(f"Requesting {route} with q_str {raw_query_param}", file=sys.stderr)
    res = get(f"{route}/?{raw_query_param}")

    headers = [
        (k, v) for k, v in res.raw.headers.items() if k.lower() not in excluded_headers
    ]
    return Response(res.content, res.status_code, headers)


@app.errorhandler(400)
def not_found(e) -> Response:
    """404 error"""
    return Response(f"""Error 404: This page is not found: {e}""", 404)
