#!/usr/bin/env python3

import os
import secrets

import fastapi
import fastapi.responses
import aioredis

import models
import storages
import providers


app = fastapi.FastAPI()
redis = aioredis.Redis(host=os.getenv('REDIS_HOST'))

Notes = storages.NoteStorage(redis)
Users = storages.UserStorage(redis)
Tokens = storages.TokenStorage(redis)

Sessions = providers.SessionProvider(Users, Tokens)


async def UserRequired(session: str = fastapi.Cookie(None)) -> models.User:
    if session is None:
        raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)

    user = await Sessions.validate(session)
    
    if user is None:
        raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)

    return user


@app.get('/api/ping/')
async def ping(
        response: fastapi.responses.JSONResponse,
):
    return {
        'response': 'pong',
    }


@app.post('/api/login/')
async def login(
        response: fastapi.responses.JSONResponse,
        credentials: models.Credentials,
):
    saved_password = await Users.search(credentials.username)

    if saved_password is None:
        if not await Users.insert(credentials.username, credentials.password):
            raise fastapi.HTTPException(fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif saved_password != credentials.password:
        raise fastapi.HTTPException(fastapi.status.HTTP_400_BAD_REQUEST)

    user = await Sessions.create(credentials)

    if user is None:
        raise fastapi.HTTPException(fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.set_cookie('session', user.session)
    
    return {
        'username': user.username,
    }


@app.get('/api/profile/')
async def profile(
        response: fastapi.responses.JSONResponse,
        user: models.User = fastapi.Depends(UserRequired),
):
    return {
        'username': user.username,
    }


@app.post('/api/logout/')
async def logout(
        response: fastapi.responses.JSONResponse,
        user: models.User = fastapi.Depends(UserRequired),
):
    await Sessions.destroy(user)
    
    response.delete_cookie('session')
    
    return {}


@app.post('/api/note/')
async def add_note(
        response: fastapi.responses.JSONResponse,
        description: models.Description,
        user: models.User = fastapi.Depends(UserRequired),
):
    tries = 16

    for _ in range(tries):
        note_id = secrets.token_hex(8)

        if await Notes.search(note_id) is None:
            break
    else:
        raise fastapi.HTTPException(fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR)

    note = models.Note(
        id=note_id,
        text=description.text,
        title=description.title,
        author=user.username,
    )

    if not await Notes.insert(note.id, note.dict()):
        raise fastapi.HTTPException(fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {
        'id': note_id,
    }


@app.get('/api/note/{note_id}/')
async def get_note(
        response: fastapi.responses.JSONResponse,
        note_id: str,
        user: models.User = fastapi.Depends(UserRequired),
):
    obj = await Notes.search(note_id)

    if obj is None:
        raise fastapi.HTTPException(fastapi.status.HTTP_404_NOT_FOUND)

    note = models.Note.parse_obj(obj)

    if note.author != user.username:
        raise fastapi.HTTPException(fastapi.status.HTTP_403_FORBIDDEN)

    return {
        'text': note.text,
        'title': note.title,
    }


@app.on_event('startup')
async def put_flag():
    flag = os.getenv('FLAG')
    username = 'admin'

    note = models.Note(
        id='flagflagflagflag',
        text=f'Good job! Here is your flag:\n{flag}',
        title='A note with flag',
        author=username,
    )

    await Users.insert(username, secrets.token_hex(8))
    await Users.persist(username)

    await Notes.insert(note.id, note.dict())
    await Notes.persist(note.id)
