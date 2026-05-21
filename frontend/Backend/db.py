import sqlite3
# DATABASE CONNECTION
def get_db():

    conn = sqlite3.connect("schedule.db")

    conn.row_factory = sqlite3.Row

    return conn