import os

import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .db import SiteRepository
from .supplies import fetch_and_parse_url, normalize_url

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
        return render_template('index.html'), 422

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


@app.route('/urls/<int:id>')
def url_details(id):
    url_data, checks = repo.get_details(id)
    return render_template('url.html', url=url_data, checks=checks)


@app.route('/urls')
def show_urls():
    urls_data = repo.get_all_urls()
    return render_template('urls.html', urls=urls_data)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = repo.get_url_by_id(id)
    
    if url:
        result = fetch_and_parse_url(url)
        if 'error' not in result:
            repo.insert_url_check(id, result)
            flash('Страница успешно проверена', 'alert-success')
        else:
            flash(result['error'], 'alert-danger')
    else:
        flash('URL не найден', 'alert-danger')
    return redirect(url_for('url_details', id=id))


@app.route('/clean-the-table')
def clean_table():
    repo.clean_table()
    flash('Таблицы успешно очищены', 'alert-success')
    return redirect(url_for('index'))