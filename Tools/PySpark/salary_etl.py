# Salary ETL Process

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
    .appName("SalaryETL") \
    .master("local[*]") \
    .getOrCreate()

# =====================================================
# READING SALARY CSV FILE
# =====================================================

salary_df = spark.read.csv(
    "../../Data/csv_data/Salary.csv",
    header=True,
    inferSchema=True
)

print("Original Salary Data")

salary_df.show(10)

# =====================================================
# HANDLING NULL VALUES
# =====================================================

salary_df = salary_df.fillna({

    "salary": 30000

})

# =====================================================
# CLEANING SALARY COLUMN
# =====================================================

salary_df = salary_df.withColumn(

    "salary",

    when(col("salary") < 0, 30000)
    .otherwise(col("salary"))

)

print("Clean Salary Data")

salary_df.show(20)

# =====================================================
# CONVERTING SPARK DATAFRAME TO PANDAS
# =====================================================

pdf = salary_df.toPandas()

# =====================================================
# SAVING CLEANED CSV FILE
# =====================================================

pdf.to_csv(

    "../../output/clean_csv/salary_clean.csv",

    index=False

)

print("Salary CSV Saved")

# =====================================================
# SAVING CLEANED EXCEL FILE
# =====================================================

pdf.to_excel(

    "../../output/clean_excel/salary_clean.xlsx",

    index=False

)

print("Salary Excel Saved")

# =====================================================
# STORING DATA INTO SQLITE DATABASE
# =====================================================

conn = sqlite3.connect("../../backend/schedule.db")

pdf.to_sql(

    "salary",

    conn,

    if_exists="replace",

    index=False

)

conn.close()

print("Salary Data Stored In SQLite")

# =====================================================
# STOPPING SPARK SESSION
# =====================================================

spark.stop()

print("Salary ETL Completed")