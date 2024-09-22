import os
import psycopg2
import requests

from flask import Flask, render_template
from flask import flash, redirect, url_for
from datetime import datetime
from bs4 import BeautifulSoup

from .database import (get_urls_post, find_all_urls,
                       find_by_id, find_checks)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connected():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def get_urls_p():
    return get_urls_post()


@app.route('/urls', methods=['GET'])
def get_urls():
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int):
    url = find_by_id(id)

    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    url = find_by_id(id)

    try:
        with requests.get(url.name) as response:
            status_code = response.status_code
            response.raise_for_status()

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return render_template('show.html', ID=id, name=url.name,
                               created_at=url.created_at,
                               checks=find_checks(id)), 422

    h1, title, description = get_seo_data(
        BeautifulSoup(response.text, 'html.parser'))

    with get_connected() as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO url_checks (url_id, status_code,\
                            h1, title, description, created_at)\
                            VALUES (%s, %s, %s, %s, %s, %s)",
                           (id, status_code, h1, title, description,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            flash('Страница успешно проверена', 'alert-success')

    return redirect(url_for('get_one_url', id=id))


def get_seo_data(html: object) -> tuple[str]:
    h1 = html.h1.get_text() if html.h1 else ''
    title = html.title.get_text() if html.title else ''

    description = html.find('meta', {'name': 'description'})
    content = description['content'] if description else ''

    return h1, title, content
