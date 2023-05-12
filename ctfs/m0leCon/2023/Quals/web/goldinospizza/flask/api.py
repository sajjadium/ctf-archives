import base64
import json
import os
import traceback
import zlib

import simple_websocket
from flask_login import current_user, login_required
from models import Order, Product, User
from server import JSONEncoder, db

from flask import Blueprint, request

api = Blueprint("api", __name__)

ok_msg = json.dumps({"ok": True})
unparsable_msg = json.dumps({"ok": False})
fail_msg = json.dumps({"ok": False, "error": "🍕"})
timeout_msg = json.dumps({"ok": False, "error": "🍕 REQUESTS TIMEOUT"})
rate_msg = json.dumps({"ok": False, "error": "TOO MANY 🍕 REQUESTS"})

max_requests = 50

# def serialize(data):
#     return base64.standard_b64encode(zlib.compress(data.encode("ascii"), level=-1)).decode("ascii")
#
#
# def unserialize(data):
#     return zlib.decompress(base64.standard_b64decode(data.encode("ascii"))).decode("ascii")


def balance(data, ws, n):
    return 1, {"ok": True, "balance": current_user.balance}


def order(data, ws, n):
    if "orders" not in data:
        raise AssertionError("NO 🍕 'orders' IN YOUR ORDER")
    if type(data["orders"]) is not list:
        raise AssertionError("NO 🍕 'orders' LIST IN YOUR ORDER")
    if n + len(data["orders"]) > max_requests:
        return len(data["orders"]), None
    for item in data["orders"]:
        if type(item) is not dict:
            db.session.rollback()
            raise AssertionError("ONE OF YOUR 🍕 ORDERS IS NOT AN ORDER")
        if "product" not in item:
            db.session.rollback()
            raise AssertionError("NO 🍕 'product' IN ONE OF YOUR ORDERS")
        if type(item["product"]) is not int:
            db.session.rollback()
            raise AssertionError("ONE OF YOUR 🍕 'product' IDS IS NOT INT")
        if "quantity" not in item:
            db.session.rollback()
            raise AssertionError("NO 🍕 'quantity' IN ONE OF YOUR ORDERS")
        if type(item["quantity"]) is not int:
            db.session.rollback()
            raise AssertionError("ONE OF YOUR 🍕 'quantity' IS NOT INT")
        product = db.session.execute(db.select(Product).filter(
            Product.id == item["product"])).scalars().one_or_none()
        if product is None:
            db.session.rollback()
            raise AssertionError("WE DON'T SELL THAT 🍕")
        quantity = item["quantity"]
        current_user.balance -= product.price * quantity
        if current_user.balance < 0:
            db.session.rollback()
            raise AssertionError("NO 🍕 STEALING ALLOWED!")
        db.session.add(Order(
            user_id=current_user.id,
            product_id=product.id,
            product_quantity=quantity,
            product_price=product.price
        ))
        if product.id == 0 and quantity > 0:
            ws.send(
                f"WOW you are SO rich! Here's a little extra with your golden special 🍕: {os.environ['FLAG']}")
    db.session.add(current_user)
    db.session.commit()
    return len(data["orders"]), {"ok": True, "balance": current_user.balance, "orders": _orders()}


def cancel(data, ws, n):
    if "orders" not in data:
        raise AssertionError("NO 🍕 'orders' TO CANCEL IN YOUR CANCEL ORDER")
    if type(data["orders"]) is not list:
        raise AssertionError(
            "NO 🍕 'orders' LIST TO CANCEL IN YOUR CANCEL ORDER")
    if n + len(data["orders"]) > max_requests:
        return len(data["orders"]), None
    for item in data["orders"]:
        if type(item) is not int:
            db.session.rollback()
            raise AssertionError("ONE OF YOUR 🍕 CANCEL ORDER IDS IS NOT INT")
        order = db.session.execute(db.select(Order).filter(
            Order.id == item, Order.user_id == current_user.id)).scalars().one_or_none()
        if order is None:
            db.session.rollback()
            raise AssertionError("YOU DID NOT ORDER THAT 🍕")
        current_user.balance += order.product_price * order.product_quantity
        db.session.delete(order)
    db.session.add(current_user)
    db.session.commit()
    return len(data["orders"]), {"ok": True, "balance": current_user.balance, "orders": _orders()}


def _orders():
    return list(map(lambda r: r._asdict(), db.session.execute(db.select(Order).filter(Order.user_id == current_user.id)).scalars().all()))


def orders(data, ws, n):
    return 1, {"ok": True, "orders": _orders()}


request_handlers = {
    "balance": balance,
    "order": order,
    "cancel": cancel,
    "orders": orders,
}


@api.route("/sock", websocket=True)
@login_required
def sock():
    ws = simple_websocket.Server(request.environ)
    try:
        i = 0
        while i < max_requests:
            n = 1
            try:
                d = ws.receive(timeout=30)
                if d is None:
                    ws.close(reason=1008, message=timeout_msg)
                    raise simple_websocket.ConnectionClosed()
                data = json.loads(d)
                if not isinstance(data, dict):
                    raise AssertionError("invalid request")
                r = data.get("request", None)
                if r not in request_handlers:
                    raise AssertionError("bad request")
                n, ret = request_handlers[r](data, ws, i)
            except json.JSONDecodeError:
                # traceback.print_exc()
                ret = unparsable_msg
            except AssertionError as e:
                # print(repr(e))
                # traceback.print_exc()
                # ret = {"ok": False}
                ret = {"ok": False, "error": str(e)}
                # ret = {"ok": False, "error": repr(e)}
                # ret = {"ok": False, "error": traceback.format_exc()}
            except simple_websocket.ConnectionClosed as e:
                raise e
            except Exception as e:
                # print(repr(e))
                traceback.print_exc()
                # ret = {"ok": False}
                # ret = {"ok": False, "error": str(e)}
                ret = {"ok": False, "error": repr(e)}
                # ret = {"ok": False, "error": traceback.format_exc()}
            if ret is not None:
                ws.send(json.dumps(ret, cls=JSONEncoder))
            else:
                ws.send(ok_msg)
            i += n
        ws.close(reason=1008, message=rate_msg)
        raise simple_websocket.ConnectionClosed()
    except simple_websocket.ConnectionClosed:
        pass
    except Exception as e:
        # print(repr(e))
        traceback.print_exc()
    return ""
