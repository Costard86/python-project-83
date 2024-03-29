import os
from flask import Flask, flash, redirect, render_template, request, url_for, abort
from dotenv import load_dotenv
from .validate_urls import normalize, validate
from .database import (get_urls, add_to_urls, get_url_by_name, get_url_by_id,
                       connection, add_to_url_checks, get_url_checks)
import requests
from requests.exceptions import RequestException
import logging
from .content_html import get_content


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')

DATABASE_URL = os.environ.get('DATABASE_URL')

SELECT_URL = 'SELECT * FROM urls WHERE name = %s;'


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('server_error.html'), 500


# main page - GET
@app.get('/')
def index():
    return render_template('index.html')


# main page - POST
@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normalized_url = normalize(url)
    error = validate(normalized_url)
    if error:
        flash(error, 'error')
        return render_template('index.html', user_input=url), 422

    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_name(conn, normalized_url)
        if found_url:
            id_found = found_url.id
            flash('Страница уже существует', 'success')
        else:
            id_found = add_to_urls(conn, normalized_url)
            flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id_found))


# all urls - GET
@app.get('/urls')
def show_urls():
    with connection(DATABASE_URL) as conn:
        all_urls = get_urls(conn)
    return render_template('all_urls.html', all_urls=all_urls)


# one url - GET
@app.get('/urls/<int:id>')
def show_url(id):
    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_id(conn, id)
        if not found_url:
            abort(404)
    return render_template('single_url.html', id=found_url.id,
                           name=found_url.name, created_at=found_url.created_at)


@app.post('/urls/<int:id>/checks')
def add_url_check(id):
    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_id(conn, id)
        status_code = -1
        h1 = ""
        title = ""
        description = ""
        if not found_url:
            abort(404)
        try:
            response = requests.get(found_url.name)
            response.raise_for_status()

            status_code = response.status_code

            h1, title, description = get_content(response.text)

            add_to_url_checks(conn, found_url.id, status_code, h1, title, description)

            flash('Проверка успешно добавлена', 'success')

        except RequestException as error:
            logging.error(f"Impossible to check {found_url.name}\n{error}")
            flash('Произошла ошибка при проверке', 'error')

        url_checks = get_url_checks(conn, found_url.id)

    return render_template('single_url.html', status_code=status_code, id=found_url.id,
                           name=found_url.name, created_at=found_url.created_at, url_checks=url_checks,
                           h1=h1, title=title, description=description)
