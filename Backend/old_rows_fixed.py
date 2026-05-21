import sqlite3

conn = sqlite3.connect("schedule.db")

cur = conn.cursor()

# =====================================================
# FIX NULL TAKEN
# =====================================================

cur.execute("""

UPDATE schedules

SET session_taken = 0

WHERE session_taken IS NULL

""")

# =====================================================
# FIX NULL LEFT
# =====================================================

cur.execute("""

UPDATE schedules

SET session_left = session_alloc

WHERE session_left IS NULL

""")

# =====================================================
# FIX NULL STATUS
# =====================================================

cur.execute("""

UPDATE schedules

SET session_status = 'Not Taken'

WHERE session_status IS NULL

""")

conn.commit()

conn.close()

print("Old rows fixed")