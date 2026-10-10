from flask import Flask, render_template, request
from jsonquerylang import jsonquery
import json
import string

app = Flask(__name__)

with open('data.json') as f:
    data = json.load(f)

def count_baby_names(name: str, year: int) -> int:
    query = f"""
                .collection
                    | filter(.Name == "{name}" and .Year == "{year}")
                    | pick(.Count)
                    | map(values())
                    | flatten()
                    | map(number(get()))
                    | sum()
            """
    output = jsonquery(data, query)
    return int(output)

def contains_digit(name: str) -> bool:
    for num in string.digits:
        if num in name:
            return True
    return False


@app.route("/", methods=["GET"])
def home():
    name = None
    year = None
    result = None
    error = None

    name = request.args.get("name", default="(no name)")
    year = request.args.get("year", type=int)

    if not name or contains_digit(name):
        error = "Please enter a name."
    elif not year:
        error = "Please enter a year."
    else:
        if year < 1880 or year > 2025:
            error = "Year must be between 1880 and 2025."
        try:
            result = count_baby_names(name=name, year=year)
        except Exception as e:
            error = f"Unexpected error: {e}"

    return render_template("index.html", name=name, year=year, count=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
