from flask import Flask, request, abort, Response
from requests import Session
from constant import routes, excluded_headers

app = Flask(__name__)

# Extra protection for my page.
banned_chars = {
    "\\",
    "_",
    "'",
    "%25",
    "self",
    "config",
    "exec",
    "class",
    "eval",
    "get",
}


def is_sus(microservice: str, cookies: dict) -> bool:
    """Check if the arguments are sus"""
    acc = [val for val in cookies.values()]
    acc.append(microservice)
    for word in acc:
        for char in word:
            if char in banned_chars:
                return True
    return False


@app.route("/", methods=["GET"])
def route_traffic() -> Response:
    """Route the traffic to upstream"""
    microservice = request.args.get("service", "homepage")

    route = routes.get(microservice, None)
    if route is None:
        return abort(404)

    # My WAF
    if is_sus(request.args.to_dict(), request.cookies.to_dict()):
        return Response("Why u attacking me???\nGlad This WAF is working!", 400)

    # Fetch the required page with arguments appended
    with Session() as s:
        for k, v in request.cookies.items():
            s.cookies.set(k, v)
        res = s.get(route, params={k: v for k, v in request.args.items()})
        headers = [
            (k, v)
            for k, v in res.raw.headers.items()
            if k.lower() not in excluded_headers
        ]

    return Response(res.content.decode(), res.status_code, headers)
