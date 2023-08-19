from aiohttp import web
from fastecdsa.curve import P256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pysm4 import encrypt_cbc
import aiofiles
import os
import json
import string
import random
import hashlib
import time
import base64

rootKey = "68acba52-7f6f-4274-ab1c-219607dd864e"
pcs = set()
base64_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/='
PKSK = {"backup":"","admin":""}

def BuildPKSK():
    global PKSK
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=rootKey.encode(),iterations=480000)
    PKSK["backup"] = kdf.derive(rootKey.encode())
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=PKSK["backup"],iterations=480000)
    PKSK["admin"] = kdf.derive(PKSK["backup"])

def mod_inv(a, m):
    return pow(a, m-2, m)

class keyGenerator(object):
    def __init__(self, seed):
        self.seed = seed
        self.P = P256.G
        # Only For Beta Version
        self.d = 0000000000000000000000000000000000000000000000000000000000000
        e = mod_inv(self.d, P256.q)
        self.Q = e * self.P

    def gen(self, seed=None):
        if seed == None:
            seed = self.seed
        r = (seed * self.P).x
        x = (r * self.Q).x
        return x & (2**(8 * 30) - 1), r

    def update(self, seed):
        self.seed = seed

def checkAuth(content):
    timestamp = int(round(time.time()) * 1000)
    if not isinstance(content,dict):
        content = json.loads(content)
    signStringEnc = base64.b64decode(content.pop('Token').encode()).decode()
    keys = sorted(content.keys())
    signString = ""
    for key in keys:
        signString += f"{key}={content[key]}&"
    md5Object = hashlib.md5()
    md5Object.update(PKSK[content["username"]])
    signValue = md5Object.hexdigest().upper()
    signString += signValue
    # Release Version a=ApplicationKey
    a = 00000000000000000000000000000000000000000000000000000000000
    a = a.to_bytes(32, 'big')
    signStringEncServer = encrypt_cbc(signString, a[:16], a[16:32])
    if signStringEncServer == signStringEnc:
        if(timestamp - int(content["timestamp"]) < 600000):
            return (content["username"],json.loads(content["data"]))
        else:
            return ("Hacker","Timeout!")
    else:
        return ("Hacker","Hacker!")

async def deepConnect(request):
    # Will be implemented in the Release Version
    # Core Code:
    # if isinstance(receiveMessage, str) and receiveMessage.startswith("XXXXXXXXXX"):
    #     command = message.split("XXXXXXXXXX")[-1]
    #     if checkAuthRes == "admin":
    #         outinfo = subprocess.getstatusoutput(("./editDatabase \"" + command + "\""))
    #         reply = ""
    #         if outinfo == None:
    #             reply = "系统无回应"
    #         else:
    #             reply = outinfo[-1]
    #         channel_send(channel, reply.replace('\n',''))
    #     elif checkAuthRes == "backup":
    #         reply = f"备份信息如下：{backupStr}"
    #         channel_send(channel, reply.replace('\n',''))
    #     else:
    #         reply = f"权限不足！"
    #         channel_send(channel, reply.replace('\n',''))

def query_parse(req):
    obj = req.query_string
    queryitem = []
    if obj:
        query = req.query.items()
        for item in query:
            queryitem.append(item)
        return dict(queryitem)
    else:
        return None

async def download(request):
    query = query_parse(request)
    try:
        params = await request.json()
    except json.decoder.JSONDecodeError:
        content = "非法的访问行为！"
        return web.Response(status=403, content_type="text/html", text=content)
    
    if params == {} or "username" not in params.keys() or "timestamp" not in params.keys() or "Token" not in params.keys():
        content = "非法的访问行为！"
        return web.Response(status=403, content_type="text/html", text=content)
    
    checkAuthRes = checkAuth(params)

    if query == None or 'file' not in query.keys():
        content = "PDC 已经记录了您这次访问行为，普通民众请勿随意访问此系统！"
        return web.Response(status=403, content_type="text/html", text=content)
    
    filename = query.get('file')
    file_dir = '/app/download'
    file_path = os.path.join(file_dir, filename)
    if (filename not in ['editDatabase','ssl.log','app']) or ((filename in ['editDatabase','app']) and (checkAuthRes[0] != 'admin')):
        async with aiofiles.open('/dev/urandom', 'rb') as f:
            content = await f.read(random.randint(2333,23333))
            if content:
                md5Object = hashlib.md5()
                md5Object.update(filename.encode())
                safeFilename = md5Object.hexdigest().upper()
                response = web.Response(
                    content_type='application/octet-stream',
                    headers={'Content-Disposition': 'attachment;filename={}'.format(safeFilename)},
                    body=content)
                return response
            else:
                return web.Response(status=404, content_type="text/html", text="文件为空")
    else:
        if os.path.exists(file_path):
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
            if content:
                response = web.Response(
                    content_type='application/octet-stream',
                    headers={'Content-Disposition': 'attachment;filename={}'.format(filename)},
                    body=content)
                return response
            else:
                return web.Response(status=404, content_type="text/html", text="文件为空")
        else:
            return web.Response(status=404, content_type="text/html", text="文件未找到")

async def index(request):
    content  = "欢迎访问行星防御理事会(PDC)面壁人作战方案管理系统！\n"
    content += "您需要进一步建立深层通信信道进行交互！ \n"
    content += "/* Beta Version */ \n"
    return web.Response(content_type="text/html", text=content)

if __name__ == "__main__":
    s = "XXX" # Only For Beta Version
    E = keyGenerator(s)
    leakFirst, newState = E.gen()
    E.update(newState)
    leakSecond, newState = E.gen()
    observed = (leakFirst << (2 * 8)) | (leakSecond >> (28 * 8))
    backupStr = f"{E.d}-{observed}"
    BuildPKSK()
    E.update(newState)
    ApplicationKey, _ = E.gen()
    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_post("/download", download)
    app.router.add_post("/deepConnect", deepConnect)
    web.run_app(
        app, access_log=None, host='0.0.0.0', port='23333'
    )