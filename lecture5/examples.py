from pyspark.sql import SparkSession

# Start a Spark session
spark = SparkSession.builder.appName("DataflowGraphExample").getOrCreate()
sc = spark.sparkContext

data = sc.parallelize(range(1, 11))  # RDD containing integers 1 to 10

mapped_data = data.map(lambda x: x ** 2)  # [1, 4, 9, ..., 100]

filtered_data = mapped_data.filter(lambda x: x > 50)  # [64, 81, 100]

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Start a Spark session
spark = SparkSession.builder.appName("DataFrameExample").getOrCreate()

# Create a DataFrame with integers from 1 to 10
data = spark.createDataFrame([(i,) for i in range(1, 11)], ["number"])

mapped_data = data.withColumn("squared", col("number") ** 2)

filtered_data = mapped_data.filter(col("squared") > 50)

grouped_data.show()
