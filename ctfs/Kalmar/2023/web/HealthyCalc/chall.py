import asyncio, os
from random import choice, randint

from celery import Celery
from flask import Flask, Blueprint, jsonify


OPERATION_SYMBOLS = {"add": "+", "sub": "-", "mult": "*"}
OPERATIONS = {
    "add": lambda lhs, rhs: cache_lookup(_add, lhs, rhs),
    "sub": lambda lhs, rhs: cache_lookup(_sub, lhs, rhs),
    "mult": lambda lhs, rhs: cache_lookup(_mult, lhs, rhs),
    # ...
}

application = Flask(__name__)
bp = Blueprint("routes", __name__)
celery = Celery(__name__)


@bp.route("/")
def index():
    op = choice(list(OPERATIONS.keys()))
    op_sym = OPERATION_SYMBOLS[op]
    a, b = randint(0, 9999), randint(0, 9999)
    return f'Hello! Want to know the result of <a href="/calc/{op}/{a}/{b}">{a} {op_sym} {b}</a>?<br/>Might take a second or two to calculate first time!'


@bp.route("/calc/<operation>/<lhs>/<rhs>")
async def calc(operation: str, lhs: int, rhs: int):
    if operation not in OPERATIONS:
        return jsonify({"err": f"Unknown operation: {operation}"})

    f = OPERATIONS[operation]
    try:
        return jsonify({"ans": await f(lhs, rhs)})
    except Exception as ex:
        return str(ex)


def gp(n) -> int:
    """ guess precision """
    if str(n).endswith(".0"):
        return int(n)
    else:
        return float(n)


async def cache_lookup(operation, lhs: int, rhs: int) -> int:
    k = f"{operation.name}_{lhs}_{rhs}"
    try:
        return gp(celery.backend.get(k))
    except:
        pass  # skip cache miss

    ans = gp(await operation(lhs, rhs))
    celery.backend.set(k, ans)
    return ans


@celery.task()
async def _add(x: int, y: int) -> int:
    return gp(x) + gp(y)


@celery.task()
async def _sub(x: int, y: int) -> int:
    return gp(x) - gp(y)


@celery.task()
async def _mult(x: int, y: int) -> int:
    return gp(x) * gp(y)


def configure_app(application, **kwargs):
    application.secret_key = os.urandom(16)
    application.config["result_backend"] = "cache+memcached://memcached:11211/"

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), application)

    application.register_blueprint(bp)


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        async def __call__(self, *args, **kwargs):
            # pretend to do heavy work
            await asyncio.sleep(1)
            with app.app_context():
                return await TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


configure_app(application, celery=celery)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, threaded=True)
