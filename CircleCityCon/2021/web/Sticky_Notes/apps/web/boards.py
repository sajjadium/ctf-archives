import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, BaseSettings, Field
from pathlib import Path
import uuid
import os
import requests

app = FastAPI()

static_path = Path(__file__).parent.absolute() / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

tmp_path = Path("/tmp/boards/")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
def index():
    return FileResponse(str(static_path / "index.html"))


@app.get("/create_board")
def create_board():
    board_id = uuid.uuid4()
    os.mkdir(tmp_path / str(board_id))
    url = app.url_path_for("board", id=str(board_id))
    return RedirectResponse(url=url)


@app.get("/board/{id}")
def board(id: uuid.UUID):
    if (tmp_path / str(id)).is_dir():
        return FileResponse(str(static_path / "board.html"))
    else:
        raise HTTPException(status_code=404, detail="That board doesn't exist")


@app.exception_handler(OSError)
def os_error_handler(request: Request, e: OSError):
    return JSONResponse(status_code=400, content={"message": str(e)})


@app.get("/board/{id}/notes")
def notes(id: uuid.UUID):
    return sorted(os.listdir(tmp_path / str(id)))


class NoteForm(BaseModel):
    id: uuid.UUID
    body: str = Field(None, min_length=1, max_length=20480)


@app.post("/board/add_note")
def add_note(form: NoteForm):
    data = notes(form.id) or []
    if len(data) >= 9:
        raise HTTPException(
            status_code=400, detail="You can't have more than 9 notes on a board"
        )

    filename = "note" + str(len(data))
    filepath = tmp_path / str(form.id) / filename
    open(filepath, "w").write(form.body)
    return filename


@app.get("/board/{id}/report")
@limiter.limit("3/minute")
def report(request: Request, id: uuid.UUID):
    bot_res = requests.get(f"http://127.0.0.1:3102/visit/{id}")
    if bot_res.status_code != 200:
        raise HTTPException(
            status_code=400, detail="The admin bot had issues reviewing the board"
        )


if __name__ == "__main__":
    uvicorn.run("boards:app", host="0.0.0.0", port=3100, workers=4)
