from flask import Flask, request, redirect, session, render_template, g
import re
import secrets
import sqlite3
import pickle
import pickletools
from db import db, append_buffer, get_buffer, is_printable, clear_buffer, register, login, set_buffer, is_using_special_buffer
from messages import *
from base64 import b64encode
from PrivateBufferClass import PrivateBufferClass
MAX_NEW_BUFFER_SIZE = 0XDD
DEFAULT_BUFFER_SIZE = 0o24


def is_safe(unsafe):
	return re.match(r"^[a-z0-9]+$", unsafe, re.I)
