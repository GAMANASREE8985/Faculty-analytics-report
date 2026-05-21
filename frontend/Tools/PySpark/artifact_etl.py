# Artifact ETL Process
import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# pyspark setup fix

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# creating folders

os.makedirs("output/clean_csv", exist_ok=True)
os.makedirs("output/clean_excel", exist_ok=True)

# spark session

spark = SparkSession.builder \
    .appName("ArtifactETL") \
    .master("local[*]") \
    .getOrCreate()

# reading artifact completed file

artifact_df = spark.read.csv(
    "../../Data/csv_data/Artifacts_Completed.csv",
    header=True,
    inferSchema=True
)

# replacing null values with zero

artifact_df = artifact_df.fillna(0)

# calculating total artifacts done by faculty

clean_df = artifact_df.groupBy(
    "faculty_id"
).agg(
    sum("count").alias("total_artifacts")
)

print("Clean Artifact Data")

clean_df.show(20)

# converting to pandas

pdf = clean_df.toPandas()

# saving csv file

pdf.to_csv(
    "output/clean_csv/artifact_clean.csv",
    index=False
)

print("Artifact CSV Saved")

# saving excel file

pdf.to_excel(
    "output/clean_excel/artifact_clean.xlsx",
    index=False
)

print("Artifact Excel Saved")

# storing in sqlite

conn = sqlite3.connect("../../schedule.db")

pdf.to_sql(
    "artifacts",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Artifact Data Stored In SQLite")

# stopping spark

spark.stop()

print("Artifact ETL Completed")