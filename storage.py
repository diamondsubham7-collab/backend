import sqlite3
import os

DB_PATH = 'wingo_stats.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT,
            game TEXT,
            prediction TEXT,
            actual TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_result(period, game, prediction, actual):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (period, game, prediction, actual)
        VALUES (?, ?, ?, ?)
    ''', (period, game, prediction, actual))
    conn.commit()
    conn.close()

def get_stats(game=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if game:
        cursor.execute('''
            SELECT COUNT(*), SUM(CASE WHEN prediction = actual THEN 1 ELSE 0 END)
            FROM results WHERE game = ?
        ''', (game,))
    else:
        cursor.execute('''
            SELECT COUNT(*), SUM(CASE WHEN prediction = actual THEN 1 ELSE 0 END)
            FROM results
        ''')
    total, correct = cursor.fetchone()
    conn.close()
    correct = correct or 0
    accuracy = round(correct / total * 100, 1) if total > 0 else 0
    return {'total': total, 'correct': correct, 'accuracy': accuracy}

init_db()