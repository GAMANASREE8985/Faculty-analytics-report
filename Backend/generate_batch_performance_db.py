import sqlite3
import random
import pandas as pd

# ==========================================
# CONNECT SQLITE DATABASE
# ==========================================

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()

# ==========================================
# DROP TABLE IF EXISTS
# ==========================================

cursor.execute("""
DROP TABLE IF EXISTS batch_student_performance
""")

# ==========================================
# CREATE TABLE
# ==========================================

cursor.execute("""
CREATE TABLE batch_student_performance (

    batch_id INTEGER,
    students_passed INTEGER,
    students_failed INTEGER,
    pass_rate REAL,
    fail_rate REAL,
    performance_status TEXT

)
""")

# ==========================================
# GET BATCH DATA
# ==========================================

df = pd.read_sql_query(
    "SELECT * FROM batches",
    conn
)

# ==========================================
# GENERATE PERFORMANCE DATA
# ==========================================

for _, row in df.iterrows():

    batch_id = row["batch_id"]

    strength = row["stu_strength"]

    # --------------------------------------
    # Students Passed
    # --------------------------------------

    students_passed = random.randint(
        int(strength * 0.40),
        int(strength * 0.98)
    )

    # --------------------------------------
    # Students Failed
    # --------------------------------------

    students_failed = (
        strength - students_passed
    )

    # --------------------------------------
    # Pass Rate
    # --------------------------------------

    pass_rate = round(
        (students_passed / strength) * 100,
        2
    )

    # --------------------------------------
    # Fail Rate
    # --------------------------------------

    fail_rate = round(
        (students_failed / strength) * 100,
        2
    )

    # --------------------------------------
    # Performance Status
    # --------------------------------------

    if pass_rate >= 90:
        status = "Excellent"

    elif pass_rate >= 75:
        status = "Good"

    elif pass_rate >= 50:
        status = "Average"

    else:
        status = "Poor"

    # --------------------------------------
    # INSERT INTO DATABASE
    # --------------------------------------

    cursor.execute("""
        INSERT INTO batch_student_performance (
            batch_id,
            students_passed,
            students_failed,
            pass_rate,
            fail_rate,
            performance_status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (

        batch_id,
        students_passed,
        students_failed,
        pass_rate,
        fail_rate,
        status

    ))

# ==========================================
# SAVE CHANGES
# ==========================================

conn.commit()

# ==========================================
# VERIFY DATA
# ==========================================

result = pd.read_sql_query("""
SELECT * FROM batch_student_performance
LIMIT 10
""", conn)

print(result)

# ==========================================
# CLOSE DATABASE
# ==========================================

conn.close()

# ==========================================
# SUCCESS MESSAGE
# ==========================================

print("\n===================================")
print("batch_student_performance")
print("TABLE CREATED SUCCESSFULLY!")
print("===================================\n")