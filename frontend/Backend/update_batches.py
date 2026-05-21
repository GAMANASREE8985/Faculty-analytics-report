import sqlite3
import random

# ==========================================
# CONNECT SQLITE DATABASE
# ==========================================

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()

# ==========================================
# UPDATE STUDENT STRENGTH
# RANDOM VALUES BETWEEN 60 TO 80
# ==========================================

cursor.execute("""
    SELECT batch_id
    FROM batches
""")

batches = cursor.fetchall()

for batch in batches:

    batch_id = batch[0]

    new_strength = random.randint(60, 80)

    cursor.execute("""
        UPDATE batches
        SET stu_strength = ?
        WHERE batch_id = ?
    """, (new_strength, batch_id))

# ==========================================
# SAVE CHANGES
# ==========================================

conn.commit()

# ==========================================
# CLOSE CONNECTION
# ==========================================

conn.close()

# ==========================================
# SUCCESS MESSAGE
# ==========================================

print("\n===================================")
print("schedule.db UPDATED SUCCESSFULLY!")
print("Student strength changed to 60-80")
print("===================================\n")