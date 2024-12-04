"""
A minimal example of a streaming pipeline in PySpark
using Structured Streaming.

(Remember to use nc -lk 9999 to run)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Create a Spark session
spark = SparkSession.builder.appName("streaming").getOrCreate()

# Define the schema of the incoming JSON data
schema = StructType([
    StructField("order_number", IntegerType()),
    StructField("item", StringType()),
    StructField("timestamp", StringType()),
    StructField("qty", IntegerType())
])

# Use local socket as a streaming source
streaming_df = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Parse the JSON data
parsed_df = streaming_df.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))

# Start the streaming query
query = parsed_df.writeStream.outputMode("append").format("console").start()

# Wait for the streaming to finish
query.awaitTermination()
