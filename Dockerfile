from python:3.8-slim-buster

workdir /app
copy requirements.txt requirements.txt

run pip install -r requirements.txt

copy . .

expose 5000

cmd ["python", "main.py"]

