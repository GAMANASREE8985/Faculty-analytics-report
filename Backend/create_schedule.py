import sqlite3

conn = sqlite3.connect("schedule.db")

cur = conn.cursor()

# =====================================================
# SCHEDULE TABLE
# =====================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS schedules(

    session_id INTEGER PRIMARY KEY AUTOINCREMENT,

    faculty_id INTEGER,

    batch_id TEXT,

    session_alloc REAL,

    session_role TEXT,

    session_date TEXT

)

""")

conn.commit()

conn.close()

print("sessions table created successfully")