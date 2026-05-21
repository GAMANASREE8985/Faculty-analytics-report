
import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# pyspark windows fix

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# creating output folders

os.makedirs("output/clean_csv", exist_ok=True)
os.makedirs("output/clean_excel", exist_ok=True)

# creating spark session

spark = SparkSession.builder \
    .appName("ScheduleETL") \
    .master("local[*]") \
    .getOrCreate()

# reading schedule csv file

schedule_df = spark.read.csv(
    "../../Data/csv_data/Schedule.csv",
    header=True,
    inferSchema=True
)

# handling null values

schedule_df = schedule_df.fillna({

    "role": "Educator",
    "session_allocated": 0

})

print("Clean Schedule Data")

schedule_df.show(20)

# converting to pandas dataframe

pdf = schedule_df.toPandas()

# saving cleaned csv

pdf.to_csv(
    "output/clean_csv/schedule_clean.csv",
  
    index=False
)

print("Schedule CSV Saved")

# saving excel file

pdf.to_excel(
    "output/clean_excel/schedule_clean.xlsx",
  
    index=False
)

print("Schedule Excel Saved")

# storing into sqlite database

# storing into sqlite database

conn = sqlite3.connect(
    "../../schedule.db"
)


# insert new rows

pdf.to_sql(

    "schedule",

    conn,

    if_exists="replace",

    index=False

)

conn.close()

print(
    "Schedule Data Stored In SQLite"
)

conn.close()

print("Schedule Data Stored In SQLite")

# stopping spark session

spark.stop()

print("Schedule ETL Completed")