import os
import psycopg2

from dotenv import load_dotenv
from flask import request, render_template, flash, redirect, url_for
from psycopg2.extras import NamedTupleCursor
from datetime import datetime

from .url import validate_url, normalize_url

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connected():
    return psycopg2.connect(DATABASE_URL)


def get_urls_post():
    url_from_request = request.form.to_dict().get('url', '')
    errors = validate_url(url_from_request)

    if len(errors) != 0:
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    new_url = normalize_url(url_from_request)

    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            try:
                cursor.execute("INSERT INTO urls (name, created_at)\
                                VALUES (%s, %s) RETURNING id",
                               (new_url,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                url_info = cursor.fetchone()
                url_id = url_info.id
                flash('Страница успешно добавлена', 'alert-success')

            except psycopg2.errors.UniqueViolation:
                url = find_by_name(new_url)
                url_id = url.id
                flash('Страница уже существует', 'alert-warning')

    return redirect(url_for('get_one_url', id=url_id))


def find_by_name(name: str):
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (name, ))
            return cursor.fetchone()


def find_all_urls():
    urls = []
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "SELECT urls.id, urls.name, \
                MAX(url_checks.created_at) AS check_time, \
                url_checks.status_code FROM urls \
                LEFT JOIN url_checks \
                ON urls.id = url_checks.url_id \
                GROUP BY urls.id, url_checks.status_code \
                ORDER BY urls.id DESC;"
            )
            urls.extend(cursor.fetchall())
    return urls


def get_one_url(id: int):
    url = find_by_id(id)

    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


def find_by_id(id: int):
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id, ))
            return cursor.fetchone()


def find_checks(url_id: int):
    url_checks = []

    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s\
                           ORDER BY id DESC",
                           (url_id, ))
            url_checks.extend(cursor.fetchall())

    return url_checks
