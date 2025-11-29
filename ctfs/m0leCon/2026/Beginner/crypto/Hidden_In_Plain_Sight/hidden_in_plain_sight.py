from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from random import Random
from starlette.middleware.sessions import SessionMiddleware
import os
from fastapi.staticfiles import StaticFiles


FLAG = os.getenv("FLAG")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", os.urandom(256).hex()))


@app.get("/api/gen")
async def gen_numbers(request: Request, cap: int = 255):
    assert 0 <= cap <= 7769
    session = request.session if hasattr(request, "session") else {}
    r = Random()
    session["guess"] = r.getrandbits(32)
    return JSONResponse(content=[r.randint(0, cap) for _ in range(64*128)])

@app.get("/api/check")
async def check_message(request: Request, value: int):
    print(f"Received guess: {value}", type(value))
    session = request.session if hasattr(request, "session") else {}
    if len(session) == 0 or "guess" not in session:
        return JSONResponse(content={"error": "No game in progress"}, status_code=400)
    if value == session["guess"]:
        session = {}
        return JSONResponse(content={"flag": FLAG})
    else:
        session = {}
        return JSONResponse(content={"result": "Incorrect guess"}, status_code=400)


app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="dist")
