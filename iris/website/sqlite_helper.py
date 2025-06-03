import os
import sqlite3

def get_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'instance', 'database.db')
    db_path = os.path.abspath(db_path)  # Clean up path (resolves '..')
    db = sqlite3.connect(db_path)
    return db