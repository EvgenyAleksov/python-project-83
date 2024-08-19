import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


# @app.route("/")
# def hello():
#    return "Hello World!"

# import os
# import psycopg2
# import requests

# from flask import Flask, render_template
# from flask import (redirect, flash, url_for, requests, abort)
# from dotenv import load_dotenv

# load_dotenv()
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# @app.route('/')
# def index():
#    return render_template('index.html')

# DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)
