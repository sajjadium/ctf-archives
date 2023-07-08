import os
import secrets
import shutil
import subprocess
from base64 import b64decode, b64encode
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, session
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

storage = Path("C:\\Temp")
storage.mkdir(exist_ok=True)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "token" in session:
            token = session["token"]
        if not token:
            raise Unauthorized("Token not set.")
        return f(token, *args, **kwargs)

    return decorator


@app.get("/")
def index():
    if not "token" in session:
        session["token"] = secrets.token_hex(16)
    return render_template("index.tpl")


def get_target(token: str, path: str) -> Path:
    base_path = storage / token
    if not base_path.exists():
        base_path.mkdir()
        for file in Path("C:\\exes").glob("*.exe"):
            if not file.name.startswith("flag"):
                shutil.copy(file, base_path)
        sample_folder = base_path / "folder"
        sample_folder.mkdir()
        (sample_folder / "test.txt").write_bytes(b64encode(b"This is a test file."))
    target = (base_path / path).resolve()
    if os.path.commonprefix([target, base_path]) != str(base_path):
        print(os.path.commonprefix([target, base_path]), base_path)
        raise BadRequest("Jailbreak!")
    return target


@app.get("/api/")
@app.get("/api/<path:subpath>")
@token_required
def list_obj(token: str, subpath: str = "."):
    target = get_target(token, subpath)
    if not target.exists():
        raise NotFound
    if target.is_file():
        if target.suffix == ".exe":
            try:
                result = subprocess.run(
                    str(target), capture_output=True, timeout=5, encoding="utf-8"
                )
                return {"output": result.stdout, "result": result.returncode}
            except Exception as e:
                return {"error": str(e)}
        else:
            # TODO: Test that this works.
            return {"content": b64decode(target.read_bytes()).decode()}
    elif target.is_dir():
        return list_dir(target)
    else:
        raise BadRequest("Invalid path.")


def list_dir(target: str):
    items = []
    for path in target.glob("*"):
        path: Path
        item = {"name": path.name}
        if path.is_symlink():
            item["type"] = "symlink"
            item["target"] = str(path.resolve())
        elif path.is_file():
            item["type"] = "file"
        elif path.is_dir():
            item["type"] = "directory"
        else:
            item["type"] = "unknown"
        items.append(item)
    return {"items": items}


@app.put("/api/")
@app.put("/api/<path:subpath>")
@token_required
def create(token: str, subpath: str = "."):
    target = get_target(token, subpath)
    object = request.json
    if "type" not in object:
        raise BadRequest("Missing type.")
    if object["type"] == "directory" and (not target.exists() or target.is_dir()):
        target.mkdir(exist_ok=True)
        return {}
    elif (
        object["type"] == "file"
        and "name" in object
        and "content" in object
        and len(object["content"]) <= 512
    ):
        if isinstance(object["content"], str):
            object["content"] = object["content"].encode()

        content = b64encode(object["content"])
        target_file = target / secure_filename(object["name"])
        if not target_file.exists() or target_file.is_file():
            target_file.write_bytes(content)
            return {"name": target_file.name}
        else:
            raise BadRequest("A object with that name already exists.")
    elif object["type"] == "symlink" and "name" in object and "target" in object:
        target_path = Path(object["target"])
        if not target_path.is_absolute():
            target_path = target / target_path
        if not target_path.exists():
            raise BadRequest("Invalid target.")
        source = target / secure_filename(object["name"])
        if not source.exists():
            source.symlink_to(target_path)
            return {"name": source.name}
        else:
            raise BadRequest("A object with that name already exists.")
    else:
        raise BadRequest("Unknown type.")


@app.delete("/api/")
@app.delete("/api/<path:subpath>")
@token_required
def delete(token: str, subpath: str = "."):
    target = get_target(token, subpath)
    if not target.exists():
        raise NotFound
    if target.is_dir():
        shutil.rmtree(target)
        return {}
    elif target.is_file() or target.is_symlink():
        target.unlink()
        return {}
    else:
        raise BadRequest("Invalid target.")


if __name__ == "__main__":
    app.run("0.0.0.0", 2753)
