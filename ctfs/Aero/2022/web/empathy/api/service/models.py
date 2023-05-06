#!/usr/bin/env python3

import pydantic


class User(pydantic.BaseModel):
    session: str
    username: str


class Note(pydantic.BaseModel):
    id: str
    text: str
    title: str
    author: str


class Credentials(pydantic.BaseModel):
    username: str = pydantic.Field(..., min_length=5)
    password: str = pydantic.Field(..., min_length=5)


class Description(pydantic.BaseModel):
    text: str = pydantic.Field(..., min_length=10)
    title: str = pydantic.Field(..., min_length=10)
