
# Batch ETL Process
import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# pyspark fix for windows

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# creating output folders

os.makedirs("output/clean_csv", exist_ok=True)
os.makedirs("output/clean_excel", exist_ok=True)

# starting spark session

spark = SparkSession.builder \
    .appName("BatchETL") \
    .master("local[*]") \
    .getOrCreate()

# reading batch csv file

batch_df = spark.read.csv(
    "../../Data/csv_data/Batch.csv",
    header=True,
    inferSchema=True
)

print("Original Batch Data")

batch_df.show(10)

# handling null values

batch_df = batch_df.fillna({

    "track_name": "Data Engineering",
    "stu_strength": 30

})

# cleaning batch names

batch_df = batch_df.withColumn(

    "batch_name",

    when(
        col("batch_name").isNull(),
        concat(lit("Batch_"), col("batch_id"))
    ).otherwise(col("batch_name"))

)

print("Clean Batch Data")

batch_df.show(20)

# converting spark dataframe to pandas

pdf = batch_df.toPandas()

# saving cleaned csv file

pdf.to_csv(

    "../../output/clean_csv/batch_clean.csv",

    index=False

)

print("Batch CSV Saved")

# saving cleaned excel file

pdf.to_excel(

    "../../output/clean_excel/batch_clean.xlsx",

    index=False

)

print("Batch Excel Saved")

# storing data into sqlite database

conn = sqlite3.connect("../../schedule.db")

pdf.to_sql(

    "batches",

    conn,

    if_exists="replace",

    index=False

)

conn.close()

print("Batch Data Stored In SQLite")

# stopping spark session

spark.stop()

print("Batch ETL Completed")