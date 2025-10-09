from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from guard.middleware import SecurityMiddleware
from guard.models import SecurityConfig
import psycopg2, subprocess, textwrap, os, json

TRUSTED_IPS = ["127.0.0.1"]

app = FastAPI()
config = SecurityConfig(
    whitelist=TRUSTED_IPS,
    blacklist=[],
)
app.add_middleware(SecurityMiddleware, config=config)

conn = psycopg2.connect("dbname=postgres")
PSQL = ["psql", "-d", "postgres", "-q"]

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "reply": None})

@app.post("/cargo/upload")
async def cargo(request: Request, note: str = Form(...)):
    sql = f"INSERT INTO notes VALUES('"+note+"');"
    proc = subprocess.run(
        PSQL,
        input=sql,
        capture_output=True,
        text=True
    )
    reply = json.dumps({
        "rc": proc.returncode,
        "out": proc.stdout,
        "err": proc.stderr,
    }, indent=2, ensure_ascii=False)
    return templates.TemplateResponse("index.html", {"request": request, "reply": reply})