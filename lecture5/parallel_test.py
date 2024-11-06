"""
A little test to show how RDDs are parallelized.
"""

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataflowGraphExample").getOrCreate()
sc = spark.sparkContext

# Modify as needed
N = 100_000_000

result = (sc
    .parallelize(range(1, N))
    # Uncomment to force only a single partition
    # .map(lambda x: (0, x))
    # .partitionBy(1)
    # .map(lambda x: x[1])
    .map(lambda x: x ** 2)
    .filter(lambda x: x >= 100 and x < 1000)
    .collect()
)

print(result)
