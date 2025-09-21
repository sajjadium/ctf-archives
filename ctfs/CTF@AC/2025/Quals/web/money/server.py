from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import os, uuid, zipfile, subprocess, json, time, html
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
app = Flask(__name__)
BASE_DIR = "/opt/app"
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
REGISTRY_PATH = os.path.join(BASE_DIR, "plugins.json")
LOG_PATH = os.path.join(BASE_DIR, "app.log")
STORE_DIR = os.path.join(BASE_DIR, "store")
os.makedirs(PLUGINS_DIR, exist_ok=True)
os.makedirs(STORE_DIR, exist_ok=True)
FLAG_ID = ""
if not os.path.exists(REGISTRY_PATH):
    with open(REGISTRY_PATH, "w") as f:
        json.dump([], f)

def log(msg):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_PATH, "a") as f:
        f.write(f"{ts} {msg}\n")

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def save_registry(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f)

@app.get("/health")
def health():
    return jsonify({"status":"ok"})

@app.get("/api/products")
def products():
    data = [
        {"id": 1, "name": "Alpha Phone", "category": "Electronics", "price": 699.0},
        {"id": 2, "name": "Beta Tablet", "category": "Electronics", "price": 499.0},
        {"id": 3, "name": "Gamma Laptop", "category": "Electronics", "price": 1299.0},
        {"id": 4, "name": "Delta Headphones", "category": "Accessories", "price": 199.0},
        {"id": 5, "name": "Epsilon Mouse", "category": "Accessories", "price": 49.0},
        {"id": 6, "name": "Zeta Keyboard", "category": "Accessories", "price": 89.0},
        {"id": 7, "name": "Eta Coffee Maker", "category": "Home Appliances", "price": 149.0},
        {"id": 8, "name": "Theta Blender", "category": "Home Appliances", "price": 99.0},
        {"id": 9, "name": "Iota Desk Chair", "category": "Furniture", "price": 259.0},
        {"id": 10, "name": "Kappa Desk", "category": "Furniture", "price": 399.0},
        {"id": 11, "name": "Lambda Sofa", "category": "Furniture", "price": 899.0},
        {"id": 12, "name": "Mu Jacket", "category": "Clothing", "price": 129.0},
        {"id": 13, "name": "Nu Sneakers", "category": "Clothing", "price": 89.0},
        {"id": 14, "name": "Xi Jeans", "category": "Clothing", "price": 59.0},
        {"id": 15, "name": "Omicron Watch", "category": "Luxury", "price": 2499.0}
    ]
    return jsonify({"items": data})

@app.get("/widget/<uid>/<path:filename>")
def widget_file(uid, filename):
    plugin_dir = os.path.join(PLUGINS_DIR, uid)
    return send_from_directory(plugin_dir, filename)

@app.get("/")
def dashboard():
    items = load_registry()
    log(items)
    cards = []
    for it in items:
        uid = it.get("uid")
        name = html.escape(it.get("name", "unknown"))
        version = html.escape(it.get("version", ""))
        author = html.escape(it.get("author", ""))
        icon = html.escape(it.get("icon", ""))
        icon_html = f'<img src="/widget/{uid}/{icon}" alt="{name}" class="card-icon">' if icon else ""
        cards.append(f"""
        <div class="card">
            {icon_html}
            <h3 class="card-title"><a class="link" href="{url_for('widget_page', uid=uid)}">{name}</a></h3>
            <p class="meta"><span class="label">Version</span><span class="value">{version}</span></p>
            <p class="meta"><span class="label">Author</span><span class="value">{author}</span></p>
        </div>
        """)
    cards_html = "\n".join(cards) if cards else "<p class='empty'>No widgets yet. Upload one or unlock the store.</p>"
    has_plugins = len(items) > 2
    store_entries = []
    if has_plugins:
        try:
            for fname in sorted(os.listdir(STORE_DIR)):
                if fname.endswith(".plugin"):
                    safe_name = html.escape(fname)
                    store_entries.append(f"""
                    <div class="card store-card">
                        <h3 class="card-title">{safe_name}</h3>
                        <a class="btn" href="{url_for('store_download', filename=fname)}">Download</a>
                    </div>
                    """)
        except Exception as e:
            log(f"store_list_error err={e}")
    store_html = ""
    if has_plugins:
        store_block = "\n".join(store_entries) if store_entries else "<p class='empty'>Refresh. Something's off.</p>"
    store_html = f"""
        <h2 class="section">Store</h2>
        <div class="cards">{store_block if has_plugins else "<p class='locked'>Sharing is caring. Upload at least one plugin to access the community vault.</p>"}</div>
    """
    return f"""<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>VC Portal</title>
            <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            :root {{
                --bg:#070311;
                --grid1:#1a0f3b;
                --grid2:#0c0520;
                --neon1:#00f0ff;
                --neon2:#ff00e6;
                --neon3:#39ff14;
                --panel:#0e0726;
                --text:#e8e8ff;
                --muted:#9aa0ff;
                --border:rgba(255,255,255,0.12);
            }}
            * {{ box-sizing:border-box }}
            html,body {{ height:100% }}
            body {{
                margin:0;
                font-family:"Press Start 2P", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
                color:var(--text);
                background:
                  radial-gradient(1200px 600px at 50% -200px, rgba(255,0,204,0.15), transparent 60%),
                  linear-gradient(180deg, rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                  repeating-linear-gradient(0deg, var(--grid2), var(--grid2) 2px, var(--grid1) 2px, var(--grid1) 4px),
                  radial-gradient(circle at 50% 120%, #120634, #070311 60%);
                overflow-x:hidden;
            }}
            .crt {{
                position:fixed; inset:0; pointer-events:none; mix-blend-mode:overlay;
                background: repeating-linear-gradient(180deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 1px, transparent 2px, transparent 4px);
                animation: flicker 3s infinite;
            }}
            @keyframes flicker {{
                0% {{ opacity:.15 }}
                50% {{ opacity:.2 }}
                100% {{ opacity:.15 }}
            }}
            .container {{ max-width:1200px; margin:0 auto; padding:24px }}
            .title {{
                font-size:28px; line-height:1.2; letter-spacing:2px; text-transform:uppercase; margin:0 0 8px;
                text-shadow:0 0 8px var(--neon1), 0 0 16px var(--neon2);
            }}
            .subtitle {{ margin:0 0 20px; font-size:12px; color:var(--muted) }}
            .panel {{
                background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
                border:1px solid var(--border);
                border-radius:14px;
                padding:16px;
                box-shadow: 0 0 20px rgba(0,255,255,0.08), inset 0 0 30px rgba(255,0,255,0.05);
                backdrop-filter: blur(4px);
            }}
            form.upload {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:18px }}
            input[type="file"] {{
                appearance:none;
                background:var(--panel);
                border:1px dashed rgba(255,255,255,0.25);
                border-radius:10px;
                padding:10px 12px;
                color:var(--text);
                max-width:100%;
            }}
            .btn {{
                display:inline-block; padding:10px 16px; border-radius:12px; text-decoration:none; font-size:12px;
                border:1px solid rgba(255,255,255,0.25);
                background: radial-gradient(120% 120% at 0% 0%, rgba(0,240,255,0.25), rgba(255,0,230,0.25));
                box-shadow: 0 0 12px rgba(0,240,255,0.35), inset 0 0 10px rgba(255,0,230,0.25);
                color:var(--text);
                transition: transform .08s ease, box-shadow .2s ease, filter .2s ease;
            }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 18px rgba(0,240,255,0.45) }}
            .btn:active {{ transform: translateY(0) scale(.99) }}
            .section {{ margin:24px 0 12px; text-shadow:0 0 6px var(--neon3) }}
            .cards {{ display:flex; flex-wrap:wrap; gap:14px }}
            .card {{
                width:220px;
                background: linear-gradient(180deg, rgba(10,4,32,0.9), rgba(6,3,20,0.9));
                border:1px solid rgba(0,240,255,0.25);
                border-radius:16px;
                padding:14px;
                box-shadow: 0 0 12px rgba(0,240,255,0.15), inset 0 0 20px rgba(255,0,230,0.05);
                transition: transform .12s ease, box-shadow .2s ease, filter .2s ease;
                text-align:center;
            }}
            .card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 24px rgba(255,0,230,0.25), 0 0 24px rgba(0,240,255,0.25) }}
            .card-icon {{ width:64px; height:64px; object-fit:contain; display:block; margin:4px auto 8px; image-rendering: pixelated }}
            .card-title {{ margin:6px 0 8px; font-size:12px; min-height:28px }}
            .meta {{ display:flex; justify-content:space-between; font-size:10px; color:var(--muted); margin:4px 0 }}
            .label {{ opacity:.8 }}
            .value {{ color:var(--text) }}
            .link {{ color:var(--neon1); text-decoration:none }}
            .link:hover {{ text-shadow:0 0 8px var(--neon1) }}
            .empty, .locked {{ color:var(--muted); font-size:12px }}
            .grid {{
                position:fixed; inset:0; z-index:-1; perspective:600px; opacity:.6;
                background:
                    linear-gradient(transparent 0 70%, rgba(0,0,0,0.6)),
                    repeating-linear-gradient(0deg, transparent, transparent 38px, rgba(0,240,255,0.12) 39px, rgba(0,240,255,0.12) 40px),
                    repeating-linear-gradient(90deg, transparent, transparent 38px, rgba(255,0,230,0.12) 39px, rgba(255,0,230,0.12) 40px);
                transform: rotateX(60deg) translateY(25vh) scale(1.2);
                filter: drop-shadow(0 0 10px rgba(0,240,255,0.35));
            }}
            .topbar {{
                display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; margin-bottom:18px
            }}
            .tagline {{ font-size:10px; color:var(--muted) }}
            .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:10px; color:var(--muted) }}
            @media (max-width:560px) {{
                .card {{ width:100% }}
                .title {{ font-size:22px }}
                .subtitle {{ font-size:11px }}
            }}
            </style>
        </head>
        <body>
            <div class="grid"></div>
            <div class="crt"></div>
            <div class="container">
                <div class="topbar">
                    <div>
                        <h1 class="title">VC Portal</h1>
                        <p class="tagline">Upload arcade-grade analytics widgets. Feed them with <span class="mono">/api/products</span>.</p>
                    </div>
                </div>
                <div class="panel">
                    <form class="upload" action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".zip,.plugin">
                        <button class="btn" type="submit">Insert Coin</button>
                    </form>
                </div>
                <h2 class="section">Widgets</h2>
                <div class="cards">{cards_html}</div>
                {store_html}
            </div>
        </body>
    </html>"""

KEY = b"SECRET_KEY!123456XXXXXXXXXXXXXXX"

def decrypt_file(input_path, output_path, key):
    with open(input_path, "rb") as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    with open(output_path, "wb") as f:
        f.write(plaintext)

@app.get("/store/download/<path:filename>")
def store_download(filename):
    items = load_registry()
    return send_from_directory(STORE_DIR, filename, as_attachment=True) if len(items)>2 else "try harder"

@app.get("/widget/<uid>")
def widget_page(uid):
    plugin_dir = os.path.join(PLUGINS_DIR, uid)
    index_html = os.path.join(plugin_dir, "index.html")
    if not os.path.exists(index_html):
        message = "missing index.html"
        return jsonify({"error":message}), 404
    return send_from_directory(plugin_dir, "index.html")

@app.post("/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error":"missing file"}), 400
    f = request.files["file"]
    if not f.filename.endswith(".plugin"):
        return jsonify({"error":".plugin file required"}), 400
    uid = str(uuid.uuid4())
    plugin_dir = os.path.join(PLUGINS_DIR, uid)
    os.makedirs(plugin_dir, exist_ok=True)
    enc_path = os.path.join(plugin_dir, f.filename)
    f.save(enc_path)
    dec_zip_path = os.path.join(plugin_dir, "plugin.zip")
    try:
        decrypt_file(enc_path, dec_zip_path, KEY)
    except Exception as e:
        log(f"decrypt_error uid={uid} err={e}")
        return jsonify({"error":"decryption failed"}), 400
    try:
        with zipfile.ZipFile(dec_zip_path, "r") as z:
            z.extractall(plugin_dir)
    except Exception as e:
        log(f"extract_error uid={uid} err={e}")
        return jsonify({"error":"bad zip"}), 400
    manifest_path = os.path.join(plugin_dir, "plugin_manifest.json")
    init_py = os.path.join(plugin_dir, "init.py")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as mf:
            manifest = json.load(mf)
    try:
        name = manifest.get("name")
        version = manifest.get("version")
        author = manifest.get("author")
        icon = manifest["icon"]
    except Exception as e:
        log(f"extract_error uid={uid} err={e}")
        return jsonify({"error":"bad manifest"}), 400
    reg = load_registry()
    reg.append({
        "uid": uid,
        "name": name,
        "version": version,
        "author": author,
        "icon": icon
    })
    save_registry(reg)
    log(f"plugin_registered uid={uid} name={name} version={version} author={author} icon={icon}")
    try:
        log(f"executing_plugin uid={uid} path={init_py}")
        r = subprocess.run(["python","init.py"], cwd=plugin_dir, capture_output=True, text=True, timeout=30)
        global FLAG_ID
        FLAG_ID = uid
        log(f"plugin_stdout uid={uid} out={r.stdout.strip()}")
        log(f"plugin_stderr uid={uid} err={r.stderr.strip()}")
    except Exception as e:
        log(f"exec_error uid={uid} err={e}")
    return redirect(url_for("dashboard"))
    
if __name__ == "__main__":
    import threading
    import time
    import requests
    def delayed_upload(plugin):
        time.sleep(5)
        try:
            files = {'file': (f'{plugin}.plugin', open(f'{STORE_DIR}/{plugin}.plugin', 'rb'))}
            response = requests.post("http://localhost:8080/upload", files=files)
        except Exception as e:
            print("Upload failed:", e)
    threading.Thread(target=delayed_upload, args=("graph",)).start()
    threading.Thread(target=delayed_upload, args=("flag",)).start()
    app.run(host="0.0.0.0", port=8080)
