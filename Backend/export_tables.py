import sqlite3
import pandas as pd
import os

# connect database
conn = sqlite3.connect("schedule.db")

# create output folder
os.makedirs("powerbi_csv", exist_ok=True)

# table names
tables = [
    
    "batches",
    "batch_student_performance",
]

# export tables
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f"powerbi_csv/{table}.csv", index=False)
    print(f"{table}.csv exported")

conn.close()

print("All tables exported successfully")