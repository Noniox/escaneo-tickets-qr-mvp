"""
Database configuration and models for the Event Access Control System
Uses SQLite for simplicity - no external database needed
"""
import sqlite3
from datetime import datetime
from pathlib import Path
import uuid as uuid_lib

# Database file path
DB_PATH = Path(__file__).parent / "invitados.db"


def get_connection():
    """Get a database connection with row factory for dict-like access"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the guests table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            email TEXT,
            asiento TEXT NOT NULL,
            checked_in INTEGER DEFAULT 0,
            checked_in_at TEXT
        )
    """)
    
    # Create index for faster UUID lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_guests_uuid ON guests(uuid)
    """)
    
    conn.commit()
    conn.close()
    print(f"[OK] Database initialized at: {DB_PATH}")


def clear_guests():
    """Remove all guests from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guests")
    conn.commit()
    conn.close()


def add_guest(nombre: str, email: str, asiento: str) -> str:
    """Add a new guest and return their UUID"""
    guest_uuid = str(uuid_lib.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO guests (uuid, nombre, email, asiento)
        VALUES (?, ?, ?, ?)
    """, (guest_uuid, nombre, email, asiento))
    
    conn.commit()
    conn.close()
    return guest_uuid


def get_guest_by_uuid(guest_uuid: str) -> dict | None:
    """Get a guest by their UUID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM guests WHERE uuid = ?", (guest_uuid,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def get_all_guests() -> list[dict]:
    """Get all guests"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM guests ORDER BY nombre")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def check_in_guest(guest_uuid: str) -> bool:
    """Mark a guest as checked in. Returns True if successful."""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    cursor.execute("""
        UPDATE guests 
        SET checked_in = 1, checked_in_at = ?
        WHERE uuid = ? AND checked_in = 0
    """, (now, guest_uuid))
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected > 0


def reset_all_checkins():
    """Reset all check-ins (useful for testing or multiple event days)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE guests SET checked_in = 0, checked_in_at = NULL")
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected


def get_stats() -> dict:
    """Get check-in statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM guests")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as checked FROM guests WHERE checked_in = 1")
    checked = cursor.fetchone()["checked"]
    
    conn.close()
    
    return {
        "total": total,
        "checked_in": checked,
        "pending": total - checked,
        "percentage": round((checked / total * 100), 1) if total > 0 else 0
    }


# Initialize database when module is imported
init_db()
