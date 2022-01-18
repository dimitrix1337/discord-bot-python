from flask import Flask
from threading import Thread

app = Flask('/')

@app.route('/')
def home():
  print("Hello, im alive.")

def run():
  app.run(host='0.0.0.0',port=8080)

def host():
  t = Thread(target=run)
  t.start()