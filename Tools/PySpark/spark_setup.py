from pyspark.sql import SparkSession

def get_spark():
    return SparkSession.builder \
        .appName("Internship_Project") \
        .master("local[*]") \
        .getOrCreate()