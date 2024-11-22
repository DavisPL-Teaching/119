"""
Some MapReduce exercises
"""

# Spark boilerplate (remember to always add this at the top of any Spark file)
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataflowGraphExample").getOrCreate()
sc = spark.sparkContext

"""
1. Among the numbers from 1 to 1000, which digit is most common?
the least common?

2. Among the numbers from 1 to 1000, written out in English, which character is most common?
the least common?

3. Does the answer change if we have the numbers from 1 to 1,000,000?
"""
