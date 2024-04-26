#!/usr/bin/env python3
from flask import Flask, send_from_directory, render_template, session, request
from flask_limiter import Limiter
from secrets import token_hex
import os
import requests
import helpers

FLAG = os.getenv("FLAG", "INS{fake_flag}")
CHALLENGE_DOMAIN = "insomnihack.flag"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or token_hex(16)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

def get_remote_address():
    return request.access_route[0]

limiter = Limiter(get_remote_address,
                  app=app,
                  default_limits=["60 per minute", "10 per second"],
                  storage_uri="memory://")

@app.route("/", methods=["GET"])
def index():
    if "subdomain" not in session:
        session["subdomain"] = token_hex(8)
    challenge_host = session["subdomain"] + "." + CHALLENGE_DOMAIN

    deployed = False
    rpc = None
    wallet = None
    contract = None
    if "instance_id" in session:
        if helpers.is_instance_running(session["instance_id"]):
            deployed = True
            rpc = session["rpc"]
            wallet = session["wallet"]
            contract = session["contract"]
        else:
            del session["instance_id"]
            del session["rpc"]
            del session["wallet"]
            del session["contract"]

    return render_template(
        "index.html",
        challenge_host=challenge_host,
        deployed=deployed,
        rpc=rpc,
        wallet=wallet,
        contract=contract,
    )


@app.route("/static/<path:path>", methods=["GET"])
def static_file(path):
    return send_from_directory("static", path)


@app.route("/domain-query", methods=["GET"])
def dns_query_get():
    domain = request.args.get("domain")
    if domain is None:
        return "Invalid request", 400

    if "instance_id" not in session:
        return "Instance not running", 400

    return helpers.resolve_domain(session["instance_id"], domain)


@app.route("/transfer-codes", methods=["GET"])
def transfer_codes():
    if "instance_id" not in session:
        return "Invalid session", 400

    contract = helpers.get_contract(session["instance_id"])
    events = contract.events.TransferInitiated().get_logs(fromBlock=0)
    transfer_codes = []
    for event in events:
        domain = event["args"]["domain"]
        recipient = event["args"]["destination"]
        code = helpers.generate_transfer_code(domain, recipient)
        transfer_codes.append({"domain": domain, "recipient": recipient, "code": code})

    return transfer_codes

@app.route("/transfer-code/<req_domain>/<req_recipient>", methods=["GET"])
def transfer_code(req_domain, req_recipient):
    if "instance_id" not in session:
        return "Invalid session", 400
    
    contract = helpers.get_contract(session["instance_id"])
    events = contract.events.TransferInitiated().get_logs(fromBlock=0)
    for event in events:
        domain = event["args"]["domain"]
        recipient = event["args"]["destination"]
        if domain == req_domain and recipient.lower() == req_recipient.lower():
            return helpers.generate_transfer_code(domain, recipient), 200
        
    return "Transfer not initiated", 401


@app.route("/send-flag", methods=["POST"])
def send_flag():
    if "subdomain" not in session:
        return "Invalid session", 400

    if "instance_id" not in session:
        return "Instance not running", 400

    port = 80
    if "port" in request.args:
        try:
            port = int(request.args["port"])
        except:
            return "Invalid port", 400

    if port < 1 or port > 65535:
        return "Invalid port", 400

    # Resolve the domain by calling the `resolveIp` function of the contract
    host = helpers.resolve_domain(
        session["instance_id"], session["subdomain"] + "." + CHALLENGE_DOMAIN
    )
    if host is None or host == "":
        return "No DNS entry for this domain", 400
    try:
        requests.post(f"http://{host}:{port}", data=FLAG, timeout=2)
    except Exception as e:
        return str(e)

    return f"Flag sent to {host}"


@app.route("/create-instance", methods=["POST"])
@limiter.limit("2 per minute; 3 per 10 minutes; 4 per 20 minutes")
def create():
    # Remark: The instance is destroyed after 20 minutes
    instance = helpers.create_instance()

    if instance["status"] == "success":
        session["instance_id"] = instance["instance_id"]
        session["rpc"] = instance["rpc"]
        session["wallet"] = instance["wallet"]
        session["contract"] = instance["contract"]

    return instance


@app.route("/stop-instance", methods=["POST"])
def stop():
    if "instance_id" in session:
        helpers.stop_instance(session["instance_id"])
        del session["instance_id"]
        del session["rpc"]
        del session["wallet"]
        del session["contract"]
        return {"status": "success", "message": "Instance stopped"}
    else:
        return {"status": "failed", "message": "No instance running"}


if __name__ == "__main__":
    app.run(debug=True)
