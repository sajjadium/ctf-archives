from fastapi import APIRouter, FastAPI

from mvmcryption.db import initialize
from mvmcryption.environ import IS_DEV
from mvmcryption.routers import auth, crypto, users

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "crypto",
        "description": "Cryptography stuff.",
    },
    {
        "name": "auth",
        "description": "Logout/Login/Register stuff.",
    },
]
app = FastAPI(
    title="Much Vulnerable Machine API",
    description="3AM Crypto chall.",
    version="dQw4w9WgXcQ",
    openapi_tags=tags_metadata,
)


if IS_DEV:
    from fastapi.middleware.cors import CORSMiddleware

    # building a frontend is left as exercise for the player
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:4200",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_event_handler("startup", initialize)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth)
api_router.include_router(crypto)
api_router.include_router(users)
app.include_router(api_router)
