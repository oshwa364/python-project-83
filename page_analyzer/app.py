import os
import random

import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .db import SiteRepository
from .supplies import normalize_url

load_dotenv() 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = SiteRepository()


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
    url_data, checks = repo.get_details(id)
    return render_template('url.html', url=url_data, checks=checks)


@app.route('/urls')
def show_urls():
    urls_data = repo.get_all_urls()
    return render_template('urls.html', urls=urls_data)


@app.post('/urls/<id>/checks')
def check_url(id):
    url_data = repo.get_details(id)
    if random.randint(1, 10) % 2 == 0:
        repo.insert_url_check(id, url_data)
        flash('Страница успешно проверена', 'alert-success')
    else:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('url_details', id=id))


@app.route('/clean-the-table')
def clean_table():
    repo.clean_table()
    return redirect(url_for('index'))