import binascii
from hashlib import sha256
from ecdsa import SigningKey
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.exceptions import HTTPException
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from concurrent.futures import ThreadPoolExecutor
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from typing import Optional
import aiosqlite
import uvicorn
import asyncio
import can
import base64
import datetime
import json
import time
import struct
import os
import hashlib
import hmac
#from aiopath import AsyncPath as Path
import asyncio
import secrets

from src import container

def recipe_context(request: Request):
    return {'recipes': request.app.state.recipes}
templates = Jinja2Templates(directory='templates', context_processors=[recipe_context])

SERVER_PORT=31337
DB_PATH=os.environ.get('DB_PATH', '/data/team_info.db')
POW_INIT_TIMEOUT=int(os.environ.get('POW_INIT_TIMEOUT', '300'))
POW_TIMEOUT=int(os.environ.get('POW_TIMEOUT', '300'))
POW_PREFIX_LEN=int(os.environ.get('POW_PREFIX_LEN', 16))
POW_DIFFICULTY=int(os.environ.get('POW_DIFFICULTY', 22))

container_action = dict()



class BusManager():
    def __init__(self, team_id, expiry):
        self.team_id = team_id
        self.bus: Optional[can.BusABC] = None
        self.websockets = list()
        self.state = dict()
        self.expiry = expiry
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.bgtasks = set()
        self.watcher = set()

    async def startup(self):
        if self.bus:
            return
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self.executor, self.setup_can_bus, loop)
        task = loop.run_in_executor(self.executor, self.read_bus, loop )
        self.bgtasks.add(task)
        task.add_done_callback(self._bus_done)
        for watcher in self.watcher:
            watcher.cancel()
        watcher = loop.create_task(self._watcher())
        self.watcher.add(watcher)
        watcher.add_done_callback(self.watcher.discard)

    async def _watcher(self):
        while True:
            await asyncio.sleep(1)
            if not self.bus:
                await self.startup()

    def _bus_done(self, task):
        self.bgtasks.discard(task)
        if self.bus:
            self.bus.shutdown()
        self.bus = None

    def setup_can_bus(self, loop):
        try:
            self.bus = can.ThreadSafeBus(
                interface="socketcan",
                channel=f'c{self.team_id}',
                fd=True, receive_own_messages=True)
            return True
        except OSError:
            return False

    def read_bus(self, loop):
        if self.bus is None:
            return

        try:
            for msg in self.bus:
                coro = self._listener(msg)
                fut = asyncio.run_coroutine_threadsafe(coro, loop)
                fut.result()
        except can.exceptions.CanOperationError:
            bus = self.bus
            self.bus = None
            bus.shutdown()

    async def _listener(self, msg):
        info = dict(
            msg="can",
            msgId=msg.arbitration_id,
            data=msg.data.hex(),
            state=self.state
        )
        match msg.arbitration_id:
            case 0x12:
                temp = struct.unpack("d", msg.data)[0]
                self.state['temp'] = f'{temp:g}'
            case 0x13:
                iid, grams = struct.unpack("<BH", msg.data[28:31])
                name = ''
                match iid:
                    case 0:
                        name = msg.data[31:].decode()
                    case 1:
                        name = 'Tomato'
                    case 2:
                        name = 'Carrot'
                    case 3:
                        name = 'Celery'
                    case 4:
                        name = 'Onion'
                    case 5:
                        name = 'Garlic'
                    case 6:
                        name = 'Sugar'
                    case 7:
                        name = 'Olive Oil'
                    case 8:
                        name = 'Salt'
                    case 9:
                        name = 'Black Pepper'
                self.state['step'] = {
                    'name': 'add',
                    'values': {
                        'name': name,
                        'grams': grams
                    }
                }
            case 0x14:
                strength, seconds = struct.unpack("<BH", msg.data[28:31])
                self.state['step'] = {
                    'name': 'mix',
                    'values': {
                        'strength': strength,
                        'seconds': seconds
                    }
                }
            case 0x15:
                degrees, seconds = struct.unpack("<HH", msg.data[28:32])
                self.state['step'] = {
                    'name': 'heat',
                    'values': {
                        'degrees': degrees,
                        'seconds': seconds
                    }
                }
            case 0x15:
                seconds = struct.unpack("<H", msg.data[28:30])[0]
                self.state['step'] = {
                    'name': 'wait',
                    'values': {
                        'seconds': seconds
                    }
                }

        for ws in self.websockets:
            await ws.send_json(info)
    
    async def send(self, arbitration_id, data):
        if arbitration_id < 0x20:
            return "Cannot send privileged Messages on Debug Interface"
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, self.bus.send,
            can.Message(arbitration_id=arbitration_id, data=data, is_fd=True))

    async def shutdown_sockets(self):
        sockets = self.websockets
        self.websockets = []
        for ws in sockets:
            await ws.close()

    def stop_bus(self):
        self.bus = None
        bus = self.bus
        print("Stopping Bus")
        bus.shutdown()
        print("Stopped")

managers = dict()

def team_id_from_token(token) -> str:
    try:
        token_bytes = base64.urlsafe_b64decode(token)
        if len(token_bytes) < 32 + 5:
            raise HTTPException(403, detail="Invalid Token")

        provided_digest = token_bytes[:32]
        new_digest = hmac.new(
            key=app.state.token_secret,
            msg=token_bytes[32:],
            digestmod=hashlib.sha256
        ).digest()
        if not hmac.compare_digest(provided_digest, new_digest):
            raise HTTPException(403, detail="Invalid Token")

        instance_id = token_bytes[32:32 + 5]
        expiry = int.from_bytes(token_bytes[32 + 5:])
        if int(time.time()) > expiry:
            raise HTTPException(403, detail="Invalid Token")
    except binascii.Error:
        raise HTTPException(403, detail="Invalid Token")
    except ValueError:
        raise HTTPException(403, detail="Invalid Token")

    return instance_id.hex()


def expiry_from_token_no_check(token) -> int:
    token_bytes = base64.urlsafe_b64decode(token)
    return int.from_bytes(token_bytes[32 + 5:])


def containers(request):
    team_id = team_id_from_token(request.path_params.get("token"))
    cmd = request.path_params.get('cmd')
    last_action = container_action.get(team_id, None)
    if not last_action:
        container_action[team_id] = datetime.datetime.now()
    else:
        now = datetime.datetime.now() 
        diff = now - last_action
        if diff.seconds < 30:
            return JSONResponse({"status": "NOK"}, status_code=429)
        container_action[team_id] = now

    if cmd in ["start", "restart", "stop", "build"]:
        container.container_state(team_id, cmd)
    return JSONResponse({"status": "OK"})


async def debug(request):
    return templates.TemplateResponse(request, 'debug.html')

async def homepage(request):
    return templates.TemplateResponse(request, 'index.html')


async def get_Manager(team_id, expiry) -> BusManager:
    manager = managers.get(team_id, None)
    if not manager:
        manager = BusManager(team_id, expiry)
        managers[team_id] = manager
        await manager.startup()
    else:
        if expiry < manager.expiry:
            raise HTTPException(403, detail="Invalid expiry")
        elif expiry > manager.expiry:
            manager.shutdown_sockets()
            manager.stop_bus()
            manager.expiry = expiry
    if not manager.bus:
        await manager.startup()
    return manager


class Team(HTTPEndpoint):
    async def get(self, request):
        team_id_from_token(request.path_params.get("token"))
        return templates.TemplateResponse(request, 'team.html')

    async def post(self, request):
        token = request.path_params.get("token")
        team_id = team_id_from_token(token)
        expiry = expiry_from_token_no_check(token)
        self.manager = await get_Manager(team_id, expiry)
        return templates.TemplateResponse(request, 'team.html')

class Consumer(WebSocketEndpoint):
    encoding = 'text'

    async def  on_connect(self, websocket):
        token = websocket.path_params.get("token")
        team_id = team_id_from_token(token)
        expiry = expiry_from_token_no_check(token)
        self.manager = await get_Manager(team_id, expiry)
        self.manager.websockets.append(websocket)
        self.team_id = team_id
        await websocket.accept()

    async def on_receive(self, websocket, data):
        cmd, value = data.split(':', 1)
        match cmd:
            case 'canframe':
                arbId, b64_msg = value.split(':',1)
                msg = base64.b64decode(b64_msg)
                ret = await self.manager.send(int(arbId), msg)
                await websocket.send_json(dict(msg="error", data=ret))
            case 'sauce':
                if value not in app.state.recipes:
                    await websocket.send_json(dict(msg="error", data="You can't cook that sauce!"))
                payload = value.encode()
                sig = app.state.signing_key.sign(payload)
                payload = sig + payload
                ret = await self.manager.send(0x20, payload)
            case _:
                await websocket.send_json(dict(msg="error",data=f"Invalid data: '{data}'"))

    async def on_disconnect(self, ws, close_code):
        if self.manager:
            self.manager.websockets.remove(ws)


async def create_new_instance_pow() -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        final_prefix = None
        for _ in range(3):
            instance_id = secrets.token_hex(5)
            prefix = secrets.token_urlsafe(POW_PREFIX_LEN)
            prefix = prefix[:POW_PREFIX_LEN].replace('-', 'B')
            prefix = prefix.replace('_', 'A')

            data = {
                'instance_id': instance_id,
                'prefix': prefix,
                'valid_until': int(time.time()) + POW_INIT_TIMEOUT,
                'pow_done': 0
            }

            try:
                await db.execute('INSERT INTO instances VALUES' +\
                    '(:instance_id, :valid_until, :prefix, :pow_done)',
                    data)
                await db.commit()
                final_prefix = prefix
            except aiosqlite.Error:
                pass

    if final_prefix is None:
        raise HTTPException(500, detail="Could not create new pow")

    return final_prefix


async def proof_of_work(request: Request):
    data = await request.json()
    if 'prefix' in data and 'answer' in data:
        # Verify hash
        h = hashlib.sha256()
        h.update((data['prefix'] + data['answer']).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        if not bits.startswith('0' * POW_DIFFICULTY):
            raise HTTPException(400, detail="Invalid answer")

        async with aiosqlite.connect(DB_PATH) as db:
            expiry = int(time.time()) + POW_TIMEOUT
            cursor = await db.cursor()
            await cursor.execute('UPDATE instances SET pow_done = ?, '+\
                'valid_until = ? WHERE prefix = ? AND pow_done = 0 ' +\
                'AND valid_until > strftime("%s", "now")', (1,
                expiry, data['prefix']))
            await db.commit()
            if cursor.rowcount != 1:
                raise HTTPException(400, detail="Invalid prefix")
            await cursor.close()
            r = await db.execute_fetchall('SELECT instance_id FROM '+\
                'instances WHERE prefix = ?', (data['prefix'],))

            instance_id = None
            for row in r:
                instance_id = row[0]
                break
            if instance_id is None:
                raise HTTPException(500, detail="Invalid instance")

            msg = bytes.fromhex(instance_id) + int.to_bytes(expiry, 4)
            token = hmac.new(
                key=request.app.state.token_secret,
                msg=msg,
                digestmod=hashlib.sha256
            ).digest() + msg
            return JSONResponse({
                'token': base64.urlsafe_b64encode(token).decode()
            })
    else:
        prefix = await create_new_instance_pow()
        return JSONResponse({
            'prefix': prefix,
            'difficulty': POW_DIFFICULTY
        })


@asynccontextmanager
async def lifespan(app: Starlette):
    token_secret = os.environ.get('TOKEN_SECRET_PATH', '/app/cookmaster/token-secret')
    def read_token_secret() -> bytes:
        with open(token_secret) as f:
            return f.read().strip().encode()
    app.state.token_secret = await asyncio.to_thread(read_token_secret)

    signing_key_path = os.environ.get('SIGNING_KEY_PATH', '/app/cookmaster/privkey')
    def read_signing_key() -> str:
        with open(signing_key_path) as f:
            return f.read()
    pem = await asyncio.to_thread(read_signing_key)
    key = SigningKey.from_pem(pem, hashfunc=sha256)
    app.state.signing_key = key

    recipe_path = os.environ.get('RECIPE_PATH', '/app/cookmaster/recipes.json')
    def read_recipes():
            with open(recipe_path) as f:
                return json.load(f)
    recipes = await asyncio.to_thread(read_recipes)
    app.state.recipes = recipes

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS instances (
                instance_id TEXT PRIMARY KEY,
                valid_until INTEGER,
                prefix TEXT UNIQUE,
                pow_done INTEGER
            )
        ''')
        await db.commit()

    #app.state.team_ids = dict()
    yield


routes = [
    Route('/{token}/container/{cmd}', containers, methods=["POST"]),
    Route('/{token}/debug', debug),
    Route('/{token}/', Team),
    Route('/', homepage),
    Route('/pow', proof_of_work, methods=["POST"]),
    WebSocketRoute('/{token}/ws', Consumer),
    WebSocketRoute('/{token}/debug', Consumer),
    Mount('/static', StaticFiles(directory='static'), name='static')
    ]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)


if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=SERVER_PORT)
