import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/phishing_simulator.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '../database/schema.sql')

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema."""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    
    conn = get_db_connection()
    
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary."""
    return dict(zip(row.keys(), row)) if row else None

def dicts_from_rows(rows):
    """Convert list of sqlite3.Row to list of dictionaries."""
    return [dict_from_row(row) for row in rows]
