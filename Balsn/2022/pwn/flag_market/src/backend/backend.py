#!/usr/bin/env python3

import os
from datetime import datetime

from flask import Flask, abort, request

def create_app():
    app = Flask(__name__)

    @app.errorhandler(Exception)
    def help(error):
        return "Try to buy a flag!\n"

    @app.route("/buy_flag", methods=["SPECIAL_METHOD_TO_BUY_FLAG"])
    def buy_flag():
        args = request.args
        data = request.form

        keys = ["card_holder", "card_number", "card_exp_year", "card_exp_month", "card_cvv", "card_money"]

        if any(k not in args for k in keys):
            abort(404)

        if "padding" not in data:
            abort(404)

        if args["card_holder"] != "M3OW/ME0W":
            abort(404)

        if args["card_number"] != "4518961863728788":
            abort(404)

        exp_date = f'{args["card_exp_month"]}/{args["card_exp_year"]}'
        card_exp = datetime.strptime(exp_date, "%m/%Y")
        if card_exp < datetime.now():
            abort(404)

        if args["card_cvv"] != "618":
            abort(404)

        if int(args["card_money"]) < 133731337:
            abort(404)

        if any(chr(c) not in data["padding"] for c in range(256)):
            abort(404)

        return f'{os.getenv("FLAG2", "BALSN{FLAG2}")}\n'

    return app

# if __name__ == '__main__':
#     app = create_app()
#     port = int(os.getenv("BACKEND_PORT", 29092))

#     app.run(host="0.0.0.0", port=port, debug=True)