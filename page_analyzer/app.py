import os

import psycopg2
import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .db import SiteRepository
from .supplies import normalize_url

load_dotenv() 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

conn = psycopg2.connect(app.config['DATABASE_URL'])
repo = SiteRepository(conn)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    raw_url = request.form['url']
    if not validators.url(raw_url):
        flash('Некорректный URL', 'alert-danger')
        return redirect(url_for('index'))

    normalized_url = normalize_url(raw_url)

    try:
        id = repo.check_existing(normalized_url)[0]
    except Exception:
        id = 0

    if id:
        flash('Страница уже существует', 'alert-info')
        redirect_url = redirect(url_for('url_details', id=id))
    else:
        url_id = repo.insert(normalized_url)
        flash('Страница успешно добавлена', 'alert-success')
        redirect_url = redirect(url_for('url_details', id=url_id))
    return redirect_url


@app.route('/urls/<id>')
def url_details(id):
    url_data = repo.get_details(id)
    return render_template('url.html', url=url_data)


@app.route('/urls')
def show_urls():
    urls_data = repo.get_all_urls()
    return render_template('urls.html', urls=urls_data)


@app.route('/urls')
def create_check():
    pass


@app.route('/clean-the-table')
def clean_table():
    repo.clean_table()
    return redirect(url_for('index'))