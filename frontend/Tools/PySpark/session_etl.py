

import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# pyspark fix for windows

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# creating folders

os.makedirs("output/clean_csv", exist_ok=True)
os.makedirs("output/clean_excel", exist_ok=True)

# starting spark

spark = SparkSession.builder \
    .appName("SessionETL") \
    .master("local[*]") \
    .getOrCreate()

# reading session file

session_df = spark.read.csv(
    "../../Data/csv_data/Session.csv",
    header=True,
    inferSchema=True
)

print("Original Session Data")

session_df.show(10)

# filling missing values

session_df = session_df.fillna({

    "session_allocated": 0,
    "session_taken": 0,
    "session_left": 0,
    "session_status": "Pending"

})

# recalculating left sessions

session_df = session_df.withColumn(

    "session_left",

    col("session_allocated") -
    col("session_taken")

)

# assigning proper status

session_df = session_df.withColumn(

    "session_status",

    when(col("session_left") == 0, "Completed")
    .when(col("session_taken") == 0, "Pending")
    .otherwise("Partial")

)

print("Clean Session Data")

session_df.show(20)

# converting to pandas dataframe

pdf = session_df.toPandas()

# saving clean csv

pdf.to_csv(

    "output/clean_csv/session_clean.csv",

    index=False

)

print("Session CSV Saved")

# saving excel file

pdf.to_excel(

    "output/clean_excel/session_clean.xlsx",

    index=False

)

print("Session Excel Saved")

# storing in sqlite

conn = sqlite3.connect("../../schedule.db")


pdf.to_sql(
    "sessions",
    conn,
    if_exists="replace",
    index=False
)


conn.close()

print("Session Data Stored In SQLite")

# stopping spark

spark.stop()

print("Session ETL Completed")