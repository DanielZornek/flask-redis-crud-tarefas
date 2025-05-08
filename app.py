from flask import Flask, render_template
import redis

red = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/criar-tarefa")
def criar_tarefa():
    return render_template('add-tarefa.html')