"""SQLite persistence. Retains the Phase 1 schema and database location."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'incidents.db'

@contextmanager
def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def initialize():
    with connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY, report TEXT NOT NULL, location TEXT NOT NULL, created TEXT NOT NULL, category TEXT DEFAULT "Unclassified", urgency TEXT DEFAULT "Not assessed", status TEXT DEFAULT "Pending review")')
        conn.execute('CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, incident_id INTEGER, created TEXT, action TEXT)')

def insert_report(report, location, created):
    with connect() as conn:
        cursor = conn.execute('INSERT INTO incidents (report, location, created) VALUES (?, ?, ?)', (report, location, created))
        incident_id = cursor.lastrowid
        conn.execute('INSERT INTO audit (incident_id, created, action) VALUES (?, ?, ?)', (incident_id, created, 'Simulated report submitted'))
        return incident_id

def list_incidents():
    with connect() as conn:
        return [dict(row) for row in conn.execute('SELECT * FROM incidents ORDER BY id DESC')]

def list_audit():
    with connect() as conn:
        return [dict(row) for row in conn.execute('SELECT * FROM audit ORDER BY id DESC')]

def save_review(incident_id, category, urgency, created):
    with connect() as conn:
        cursor = conn.execute('UPDATE incidents SET category=?, urgency=?, status=? WHERE id=?', (category, urgency, 'Reviewed', incident_id))
        if cursor.rowcount != 1:
            raise ValueError('Incident not found.')
        conn.execute('INSERT INTO audit (incident_id, created, action) VALUES (?, ?, ?)', (incident_id, created, f'Manual review: {category}; {urgency}'))
