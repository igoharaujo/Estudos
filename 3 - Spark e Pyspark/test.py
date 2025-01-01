from pyspark.sql import SparkSession

# Cria uma SparkSession
spark = SparkSession.builder.appName("Spark Submit").getOrCreate()