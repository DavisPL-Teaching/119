"""
This is an example which shows how to create a data frame from a Python dict.
"""

# Boilerplate
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
sc = spark.sparkContext

# Dataset
people = spark.createDataFrame([
    {"deptId": 1, "age": 40, "name": "Hyukjin Kwon", "gender": "M", "salary": 50},
    {"deptId": 1, "age": 50, "name": "Takuya Ueshin", "gender": "M", "salary": 100},
    {"deptId": 2, "age": 60, "name": "Xinrong Meng", "gender": "F", "salary": 150},
    {"deptId": 3, "age": 20, "name": "Haejoon Lee", "gender": "M", "salary": 200}
])

people_filtered = people.filter(people.age > 30)

people_filtered.show()

people2 = sc.parallelize([
    {"deptId": 1, "age": 40, "name": "Hyukjin Kwon", "gender": "M", "salary": 50},
    {"deptId": 1, "age": 50, "name": "Takuya Ueshin", "gender": "M", "salary": 100},
    {"deptId": 2, "age": 60, "name": "Xinrong Meng", "gender": "F", "salary": 150},
    {"deptId": 3, "age": 20, "name": "Haejoon Lee", "gender": "M", "salary": 200}
])

people2_filtered = people2.filter(lambda x: x["age"] > 30)

result = people2_filtered.collect()

print(result)
