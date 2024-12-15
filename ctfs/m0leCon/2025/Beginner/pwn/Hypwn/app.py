from flask import Flask, session, redirect, url_for, render_template, request, jsonify, abort
import uuid
import subprocess
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.template_folder = "templates"
app.static_url_path = "/static"
app.static_folder = "assets"

# Predefined Pokemon movesets
MULE_SET = {
    "Snorlax": ["Protect", "Recover", "Headbutt", "GigaImpact"],
    "Lucario": ["CalmMind", "AuraSphere", "GigaImpact", "Protect"],
}

@app.route("/")
def index():
    session.clear()
    return render_template("menu.html")

@app.route("/play", methods=["POST"])
def play():
    trainer_name = request.form.get("trainerName")
    selected_pokemon = request.form.get("selectedPokemon")

    if not selected_pokemon or selected_pokemon not in MULE_SET:
        return abort(400, "Invalid Pokemon selection.")

    opponent_pokemon = random.choice(["Arceus", "Mewtwo"])

    session.clear()
    session.update({
        "id": str(uuid.uuid4()),
        "allyName": selected_pokemon,
        "opponentName": opponent_pokemon,
        "allyHP": 100,
        "opponentHP": 100,
        "allyBurnt": 0,
        "allyCanMove": 1,
        "allyAttackMultiplier": 1,
        "allyHasProtected": 0,
        "opponentAttackMultiplier": 1
    })

    return render_template(
        "pokemon.html", 
        selectedPokemon=selected_pokemon, 
        opponentPokemon=opponent_pokemon, 
        moveset=MULE_SET[selected_pokemon]
    )

@app.route("/battle", methods=["GET"])
def battle():
    try:
        selected_move = request.args.get("selectedMove", "").strip()
        ally_pokemon = session.get("allyName")

        if not ally_pokemon or selected_move not in MULE_SET.get(ally_pokemon, []):
            return abort(400, "Invalid move or Pokemon.")

        opponent_pokemon = session.get("opponentName")
        if not opponent_pokemon:
            return abort(400, "Session data missing.")

        # Prepare subprocess arguments
        battle_args = [
            "./battle",
            ally_pokemon,
            str(session.get("allyHP")),
            str(session.get("allyBurnt")),
            str(session.get("allyCanMove")),
            str(session.get("allyAttackMultiplier")),
            str(session.get("allyHasProtected")),
            selected_move,
            opponent_pokemon,
            str(session.get("opponentHP")),
            str(session.get("opponentAttackMultiplier"))
        ]

        result = subprocess.run(battle_args, capture_output=True, text=True, check=True).stdout.splitlines()
        for line in result:
            if line.startswith(f"{ally_pokemon}:"):
                values = list(map(int, line.split(":")[1].split(", ")))
                session.update({
                    "allyHP": values[0],
                    "allyBurnt": values[1],
                    "allyCanMove": values[2],
                    "allyAttackMultiplier": values[3],
                    "allyHasProtected": values[4]
                })
            elif line.startswith(f"{opponent_pokemon}:"):
                values = list(map(int, line.split(":")[1].split(", ")))
                session["opponentHP"] = values[0]
                session["opponentAttackMultiplier"] = values[1]

        output = {
            "message": result[:-3],  # Exclude updated HP values
            "allyHP": session["allyHP"],
            "opponentHP": session["opponentHP"]
        }

        if "GAME OVER" in result:
            session.clear()

        return jsonify(output)

    except subprocess.CalledProcessError:
        return abort(500, "Battle simulation failed.")
    except Exception:
        return abort(400, "Invalid request data.")

if __name__ == "__main__":
    app.run(debug=False, port=2222, threaded=True)
