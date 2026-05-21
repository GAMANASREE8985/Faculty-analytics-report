import os
import sqlite3

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, concat, lower, lit, initcap

# PySpark setup
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# Create folders
os.makedirs("../../output/clean_csv", exist_ok=True)
os.makedirs("../../output/clean_excel", exist_ok=True)

# Start Spark
spark = SparkSession.builder \
    .appName("EmployeeETL") \
    .master("local[*]") \
    .getOrCreate()

print("Spark Started")

# Read employee csv file
emp_df = spark.read.csv(
    "../../Data/csv_data/Employee.csv",
    header=True,
    inferSchema=True
)

print("Original Employee Data")
emp_df.show(10)

# Fill missing values
emp_df = emp_df.fillna({
    "name": "Unknown",
    "city": "Bangalore",
    "state": "KA",
    "doj": "2024-01-01"
})

# Create email if missing
emp_df = emp_df.withColumn(
    "mail",
    when(
        (col("mail") == "") | col("mail").isNull(),
        concat(
            lower(col("name")),
            lit("."),
            col("emp_id").cast("string"),
            lit("@company.com")
        )
    ).otherwise(col("mail"))
)

# Format employee names
emp_df = emp_df.withColumn(
    "name",
    initcap(col("name"))
)

print("Clean Employee Data")
emp_df.show(20)

# Convert Spark DataFrame to Pandas
pdf = emp_df.toPandas()

# Save cleaned csv
pdf.to_csv(
    "../../output/clean_csv/employee_clean.csv",

    index=False
)

print("CSV File Saved")

# Save excel file
pdf.to_excel(
    "../../output/clean_excel/employee_clean.xlsx",

    index=False
)

print("Excel File Saved")

# Store data in SQLite database
conn = sqlite3.connect("../../schedule.db")

pdf.to_sql(
    "employees",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Data Stored in SQLite")

# Stop Spark session
spark.stop()

print("Employee ETL Process Completed")
