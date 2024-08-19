import os
import psycopg2

from flask import Flask, render_template
from dotenv import load_dotenv
# from datetime import datetime
# from psycopg2.extras import NamedTupleCursor


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)


def get_connected():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/')
def urls():
    return render_template('urls.html')


# import requests
# from flask import (redirect, flash, url_for, requests, abort)
