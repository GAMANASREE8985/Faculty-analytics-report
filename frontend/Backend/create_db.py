
# CREATE DATABASE TABLES


import sqlite3

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()
# EMPLOYEE TABLE
cursor.execute("""

CREATE TABLE IF NOT EXISTS employees(

    emp_id INTEGER PRIMARY KEY,

    name TEXT,

    mail TEXT,

    type TEXT,

    city TEXT,

    state TEXT,

    doj TEXT

)

""")
# EMP POSITION TABLE
cursor.execute("""

CREATE TABLE IF NOT EXISTS emp_position(

    faculty_id INTEGER,

    position TEXT

)

""")
# SESSION TABLE


cursor.execute("""

CREATE TABLE IF NOT EXISTS sessions(

    session_id INTEGER,

    faculty_id INTEGER,

    batch INTEGER,

    date TEXT,

    alloc REAL,

    taken REAL,

    left REAL,

    status TEXT,

    sch_id INTEGER

)

""")

# ARTIFACT TABLE
cursor.execute("""

CREATE TABLE IF NOT EXISTS artifacts(

    faculty_id INTEGER,

    total_qp INTEGER,

    total_capstone INTEGER,

    total_courses INTEGER,

    total_cert INTEGER,

    total_tools INTEGER,

    grand_total INTEGER

)

""")

conn.commit()

conn.close()

print("✅ DATABASE CREATED")