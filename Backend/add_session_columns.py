import sqlite3

conn = sqlite3.connect("schedule.db")

cur = conn.cursor()

# =====================================================
# ADD session_taken COLUMN
# =====================================================

try:

    cur.execute("""

    ALTER TABLE schedules

    ADD COLUMN session_taken REAL

    """)

    print("session_taken added")

except:

    print("session_taken already exists")


# =====================================================
# ADD session_left COLUMN
# =====================================================

try:

    cur.execute("""

    ALTER TABLE schedules

    ADD COLUMN session_left REAL

    """)

    print("session_left added")

except:

    print("session_left already exists")


# =====================================================
# ADD session_status COLUMN
# =====================================================

try:

    cur.execute("""

    ALTER TABLE schedules

    ADD COLUMN session_status TEXT

    """)

    print("session_status added")

except:

    print("session_status already exists")


conn.commit()

conn.close()

print("Database Updated Successfully")