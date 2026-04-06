import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class SiteRepository:
    def __init__(self):
        pass

    def check_existing(self, url):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
                return cur.fetchone()

    def insert(self, url):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('''
                    INSERT INTO urls (name, created_at) 
                    VALUES (%s, %s) RETURNING id
                    ''',
                    (url, datetime.now())
                )
                return cur.fetchone()['id']
            
    def get_url_by_id(self, url_id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
                url = cur.fetchone()['name']
                return url
        
    def get_details(self, url_id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
                url_data = cur.fetchone()
                cur.execute('''
                    SELECT * FROM url_checks
                    WHERE url_id = %s 
                    ORDER BY created_at DESC
                    ''',
                    (url_id,)
                )
                check_data = cur.fetchall()
                return url_data, check_data
        
    def get_all_urls(self):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('''
                    SELECT u.id, u.name, MAX(c.created_at) AS last_checked,
                            MAX(c.status_code) AS last_status_code
                    FROM urls u
                    LEFT JOIN url_checks c ON u.id = c.url_id
                    GROUP BY u.id
                    ORDER BY u.created_at DESC
                ''')
                return cur.fetchall()
    
    def insert_url_check(self, url_id, data):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('''
                    INSERT INTO url_checks 
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (url_id, data['status_code'], data['h1'],
                    data['title'], data['description'], datetime.now())
                )

    def clean_table(self):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('TRUNCATE TABLE urls RESTART IDENTITY CASCADE')