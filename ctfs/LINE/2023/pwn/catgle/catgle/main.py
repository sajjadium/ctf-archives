from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette_validation_uploadfile import ValidateUploadFileMiddleware

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router
from domain.chall import chall_router

from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models
from database import engine

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/",
        max_size=1024 * 1024 * 101, #100Mbyte
        file_type=["*"]
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(chall_router.router)


app.mount("", StaticFiles(directory="frontend/", html=True), name="frontend")
# to support Browser Routing of routify in frontend
templates = Jinja2Templates(directory="frontend/")
@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    return templates.TemplateResponse("index.html", {"request": request})
