from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

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
        
    def get_details(self, url_id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
                url_data = cur.fetchone()
                return url_data
        
    def get_all_urls(self):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('''
                SELECT u.id, u.name
                FROM urls u
                ORDER BY u.created_at DESC
                ''')
                return cur.fetchall()
        
    def clean_table(self):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('TRUNCATE TABLE urls RESTART IDENTITY')