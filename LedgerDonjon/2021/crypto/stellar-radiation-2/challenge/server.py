#!/usr/bin/env python
import os
import string

from aiohttp import web
from stellar_sdk import (
    Keypair,
    Account,
    TransactionBuilder,
    Asset,
    Network,
    TransactionEnvelope,
)
from stellar_sdk.exceptions import BadSignatureError

app = web.Application()
routes = web.RouteTableDef()


STELLAR_SECRET = os.environ.get("STELLAR_SECRET")
FLAG = os.environ.get("FLAG")
if STELLAR_SECRET is None or FLAG is None:
    raise EnvironmentError("Secrets are not set")


# Disabled for now
# @routes.post("/prepareorder")
async def prepare_order(request: web.Request):
    data = await request.post()
    if "address" not in data:
        return web.Response(status=500, body="Missing destination address")

    keypair = Keypair.from_secret(STELLAR_SECRET)
    account = Account(account=keypair.public_key, sequence=1)

    transaction = (
        TransactionBuilder(
            source_account=account,
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        .append_payment_op(
            data["address"], Asset("PIZZA", keypair.public_key), "1"
        )
        .build()
    )
    transaction.sign(keypair)
    return web.Response(body=transaction.to_xdr())


@routes.post("/submit")
async def submit_transaction(request: web.Request):
    data = await request.post()
    if "tx" not in data:
        return web.Response(status=500, body="Missing tx")
    envelope = TransactionEnvelope.from_xdr(
        data["tx"], Network.PUBLIC_NETWORK_PASSPHRASE
    )
    if len(envelope.signatures) != 1:
        return web.Response(status=500, body="Invalid envelope")
    keypair = Keypair.from_secret(STELLAR_SECRET)
    try:
        keypair.verify(envelope.hash(), envelope.signatures[0].signature)
    except BadSignatureError:
        return web.Response(status=500, body="Invalid signature")
    # server = Server(horizon_url="https://horizon.stellar.org")
    # response = server.submit_transaction(envelope)
    # return response["flag"]
    return web.Response(body=FLAG)


MAX_PROOF_SIZE = 32
MAX_TRIES = 30


@routes.post("/publickey")
async def public_key(request: web.Request):
    data = await request.post()
    public_keys = set()

    # Detect Stellar radiations
    for _ in range(MAX_TRIES):
        public_keys.add(Keypair.from_secret(STELLAR_SECRET).public_key)
        if len(public_keys) > 1:
            return web.Response(status=500)

    sk = Keypair.from_secret(STELLAR_SECRET).signing_key
    if "proof" in data:
        # Sign a short "proof" message so that client can verify public key is valid,
        # in case previous check was not enough.
        # Proof must be short, printable messages.
        proof = data["proof"]
        if len(proof) > MAX_PROOF_SIZE or not all(c in string.printable for c in proof):
            return web.Response(status=500, body="Invalid proof requested")
        signed_message = sk.sign(proof.encode())
        return web.json_response(
            {
                "public_key": public_keys.pop(),
                "signature": signed_message.signature.hex(),
            }
        )
    else:
        return web.json_response({"public_key": public_keys.pop()})


@routes.get("/")
async def index(request):
    return web.FileResponse("./index.html")


if __name__ == "__main__":
    app.add_routes(routes)
    web.run_app(app, port=25520)
