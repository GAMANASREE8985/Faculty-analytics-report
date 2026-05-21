import sqlite3

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM Schedules")


conn.commit()

print("Old schedules deleted successfully!")

conn.close()