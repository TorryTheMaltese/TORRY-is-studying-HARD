from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import errors


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        name = 'Stranger'
    elif request.method == 'GET':
        name = request.args.get('name')
    return render_template('index.html', name=name)
