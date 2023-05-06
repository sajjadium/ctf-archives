import uvicorn
from fastapi import FastAPI, File, Query
import os
from pathlib import Path
import subprocess
import requests

UPLOADS_DIR = Path(os.environ["UPLOADS_DIR"])
APP_URL = os.environ["APP_URL"]
BOT_URL = os.environ["BOT_URL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]


app = FastAPI()


@app.post("/upload_ipynb/")
async def upload_ipynb(file: bytes = File(...)):
    filename = os.urandom(16).hex() + ".ipynb"
    filepath = UPLOADS_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file)

    subprocess.run(f"jupyter trust {filepath}", shell=True)
    url = f"{APP_URL}:8888/notebooks/{filename}"

    data = {"url": url, "token": BOT_TOKEN}
    res = requests.post(f"{BOT_URL}/visit", json=data)
    return {"url": url, "bot_status_code": res.status_code}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", root_path="/api", port=3000, workers=4)
