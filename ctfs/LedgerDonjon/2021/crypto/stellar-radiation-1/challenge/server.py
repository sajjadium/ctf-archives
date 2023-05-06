#!/usr/bin/env python
import os

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


@routes.get("/publickey")
async def public_key(_: web.Request):
    keypair = Keypair.from_secret(STELLAR_SECRET)
    return web.Response(body=keypair.public_key)


@routes.get("/")
async def index(request):
    return web.FileResponse("./index.html")


if __name__ == "__main__":
    app.add_routes(routes)
    web.run_app(app, port=25519)
