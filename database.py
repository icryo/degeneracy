import sqlite3
from contextlib import closing

DATABASE_FILE = "csfloat_bot.db"

def initialize_db():
    """Ensure the database has the required table."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_listings (
                id TEXT PRIMARY KEY,
                created_at TEXT
            )
        """)
        conn.commit()

def store_listing(listing_id, created_at):
    """Store a new listing in the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO seen_listings (id, created_at)
            VALUES (?, ?)
        """, (listing_id, created_at))
        conn.commit()

def is_listing_seen(listing_id):
    """Check if a listing_id exists in the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT 1 FROM seen_listings WHERE id = ?", (listing_id,))
            return cursor.fetchone() is not None

def mark_listing_as_seen(listing_id, created_at):
    """Insert a listing_id into the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
                INSERT OR IGNORE INTO seen_listings (id, created_at)
                VALUES (?, ?)
            """, (listing_id, created_at))
        conn.commit()
