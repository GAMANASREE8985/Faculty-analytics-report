# Self Development ETL Process

import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# =====================================================
# PYSPARK FIX FOR WINDOWS
# =====================================================

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# =====================================================
# CREATING OUTPUT FOLDERS
# =====================================================

os.makedirs("../../output/clean_csv", exist_ok=True)
os.makedirs("../../output/clean_excel", exist_ok=True)

# =====================================================
# STARTING SPARK SESSION
# =====================================================

spark = SparkSession.builder \
    .appName("SelfDevelopmentETL") \
    .master("local[*]") \
    .getOrCreate()

# =====================================================
# READING SELF DEVELOPMENT CSV FILE
# =====================================================

self_df = spark.read.csv(
    "../../Data/csv_data/Self_Development.csv",
    header=True,
    inferSchema=True
)

print("Original Self Development Data")

self_df.show(10)

# =====================================================
# HANDLING NULL VALUES
# =====================================================

self_df = self_df.fillna({

    "internal_certification": 0,
    "external_certification": 0

})

# =====================================================
# CLEANING CERTIFICATION VALUES
# =====================================================

self_df = self_df.withColumn(

    "internal_certification",

    when(col("internal_certification") < 0, 0)
    .otherwise(col("internal_certification"))

)

self_df = self_df.withColumn(

    "external_certification",

    when(col("external_certification") < 0, 0)
    .otherwise(col("external_certification"))

)

print("Clean Self Development Data")

self_df.show(20)

# =====================================================
# CONVERTING SPARK DATAFRAME TO PANDAS
# =====================================================

pdf = self_df.toPandas()

# =====================================================
# SAVING CLEANED CSV FILE
# =====================================================

pdf.to_csv(

    "../../output/clean_csv/self_development_clean.csv",

    index=False

)

print("Self Development CSV Saved")

# =====================================================
# SAVING CLEANED EXCEL FILE
# =====================================================

pdf.to_excel(

    "../../output/clean_excel/self_development_clean.xlsx",

    index=False

)

print("Self Development Excel Saved")

# =====================================================
# STORING DATA INTO SQLITE DATABASE
# =====================================================

conn = sqlite3.connect("../../backend/schedule.db")

pdf.to_sql(

    "self_development",

    conn,

    if_exists="replace",

    index=False

)

conn.close()

print("Self Development Data Stored In SQLite")

# =====================================================
# STOPPING SPARK SESSION
# =====================================================

spark.stop()

print("Self Development ETL Completed")