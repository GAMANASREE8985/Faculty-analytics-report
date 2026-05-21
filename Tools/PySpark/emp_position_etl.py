# =========================================================
# Emp Position ETL Process
# =========================================================

import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# pyspark windows fix

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# creating folders

os.makedirs("../../output/clean_csv", exist_ok=True)
os.makedirs("../../output/clean_excel", exist_ok=True)

# spark session

spark = SparkSession.builder \
    .appName("EmpPositionETL") \
    .master("local[*]") \
    .getOrCreate()

# reading employee position file

position_df = spark.read.csv(
    "../../Data/csv_data/Emp_Position.csv",
    header=True,
    inferSchema=True
)

print("Original Employee Position Data")

position_df.show(10)

# handling null values

position_df = position_df.fillna({

    "position": "Faculty"

})

# cleaning duplicate spaces

position_df = position_df.withColumn(

    "position",

    trim(col("position"))

)

print("Clean Employee Position Data")

position_df.show(20)

# converting to pandas

pdf = position_df.toPandas()

# saving csv

pdf.to_csv(
    "../../output/clean_csv/emp_position_clean.csv",
    index=False
)

print("Emp Position CSV Saved")

# saving excel

pdf.to_excel(
    "output/clean_excel/emp_position_clean.xlsx",
    index=False
)

print("Emp Position Excel Saved")

# storing into sqlite

conn = sqlite3.connect("../../schedule.db")

pdf.to_sql(
    "emp_position",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Emp Position Data Stored In SQLite")

# stopping spark

spark.stop()

print("Emp Position ETL Completed")