#!/bin/sh

export PATH

cp /app/tmp/* /app/quizzes
cd /app/quizzes
python3 -B ../main.py

