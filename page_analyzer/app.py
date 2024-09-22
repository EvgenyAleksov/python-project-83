import os

from flask import Flask, render_template

from .database import (get_urls_p, find_all_urls, get_one_ur, check_ur)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def get_urls_post():
    return get_urls_p()


@app.route('/urls', methods=['GET'])
def get_urls():
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int):
    return get_one_ur(id)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    return check_ur(id)
