import psycopg2
import json
from config import DB_CONFIG

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            id SERIAL PRIMARY KEY,
            template_name TEXT,
            style TEXT,
            structure JSONB
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_template(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO templates (template_name, style, structure) VALUES (%s, %s, %s)",
        (data['templateName'], data['style'], json.dumps(data))
    )
    conn.commit()
    cur.close()
    conn.close()

def get_templates():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT structure FROM templates")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
