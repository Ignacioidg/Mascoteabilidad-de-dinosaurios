import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'dinomascota.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
SEEDS_PATH = os.path.join(DB_DIR, 'seeds.sql')

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db(force_reload: bool = False):
    db_exists = os.path.exists(DB_PATH)
    if force_reload or not db_exists:
        conn = get_connection()
        cursor = conn.cursor()
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        with open(SEEDS_PATH, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
        print('[DB] Base de datos dinomascota.db inicializada con exito.')
    else:
        print('[DB] Base de datos existente encontrada.')

def query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

def query_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == '__main__':
    init_db(force_reload=True)
