#!/bin/bash

mkdir chani-ai
cd chani-ai

touch chani.py
touch requirements.txt
touch README.md

echo "fastapi
uvicorn
openai
python-dotenv" > requirements.txt

git init
git add .
git commit -m "ChaNi AI Platform"

gh repo create chani-ai --public --source=. --push
