from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'