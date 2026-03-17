from datetime import datetime

from psycopg2.extras import RealDictCursor


class SiteRepository:
    def __init__(self, conn):
        self.conn = conn

    def check_existing(self, url):
        with self.conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
            return cur.fetchone()

    def insert(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                INSERT INTO urls (name, created_at) 
                VALUES (%s, %s) RETURNING id
                ''',
                (url, datetime.now())
            )
            self.conn.commit()
            return cur.fetchone()['id']
        
    def get_details(self, url_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
            url_data = cur.fetchone()
            return url_data
        
    def get_all_urls(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
            SELECT u.id, u.name
            FROM urls u
            ORDER BY u.created_at DESC
            ''')
            return cur.fetchall()
        
    def clean_table(self):
        with self.conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE urls RESTART IDENTITY')
            self.conn.commit()