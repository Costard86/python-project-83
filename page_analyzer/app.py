import os
import psycopg2
from flask import Flask, flash, redirect, render_template, request, url_for, abort
from dotenv import load_dotenv
from .validate_urls import normalize, validate
import datetime as dt
from flask.helpers import get_flashed_messages
import contextlib


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')

DATABASE_URL = os.environ.get('DATABASE_URL')

SELECT_URL = 'SELECT * FROM urls WHERE name = %s;'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the url from the form is correct
        url = request.form.get('url')
        normalized_url = normalize(url)
        error = validate(normalized_url)
        if error:
            flash(error, 'error')
            return render_template('index.html', user_input=url), 422

        with connection(DATABASE_URL) as conn:
            found_url = check_name_exists(conn, normalized_url)
            if found_url:
                id = found_url
                flash('Страница уже существует', 'success')
            else:
                id = add_name_to_urls(conn, normalized_url)
                flash('Страница успешно добавлена', 'success')
        return redirect(url_for('index'))

    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


def check_name_exists(conn, name):
     with conn.cursor() as curs:
         curs.execute(SELECT_URL, (name,))
         result = curs.fetchone()

     return result


def add_name_to_urls(conn, name):
    with conn.cursor() as curs:
        curs.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;", (name, dt.datetime.now()))
        returned_id = curs.fetchone()[0]

    return returned_id


@contextlib.contextmanager
def connection(db_url):
    conn = psycopg2.connect(db_url)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()
