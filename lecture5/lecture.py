"""
Lecture 5: Distributed Pipelines

Agenda:

- Recap: on dataflow graphs

- Scalable collection types

- Programming over collection types

Possible topics/optional:

- Throughput and latency model

- Partitioning strategies

- Distributed consistency: crashes, failures, duplicated/dropped messges

- Pitfalls
"""

"""
In this lecture, we will use Apache Spark (PySpark).

Spark is a parallel and distributed data processing framework.

(Note: Spark also has APIs in several other languages, most typically
Scala and Java. The Python version aligns best with the sorts of
code we have been writing so far and is generally quite accessible.)

Documentation:
https://spark.apache.org/docs/latest/api/python/index.html

To test whether you have PySpark installed successfully, try running
the lecture now:

python3 lecture.py
"""

# Test whether import works
import pyspark

# All spark code generally starts with the following setup code:
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataflowGraphExample").getOrCreate()
sc = spark.sparkContext

"""
Motivation: last lecture (over the last couple of weeks) we saw that:

- Parallelism can exist in many forms (hard to identify and exploit!)

- Concurrency can lead to a lot of trouble (naively trying to write concurrent code can lead to bugs)

- Parallelism alone (without distribution) can only scale your compute, and only by a limited amount (limited by your CPU bandwidth, # cores, and amount of RAM on your laptop!)

We want to be able to scale pipelines automatically to larger datasets.
How?

Idea:

- **Build our pipelines** at a higher level of abstraction -- build data sets and operators over data sets

- **Deploy our pipelines** using a framework or library that will automatically scale and take advantage of parallel and distributed compute resources.

Analogy: kind of like a compiler or interpreter!
    (A long time ago, people use to write all code in assembly language/
    machine code)

So what is that higher level abstraction?

SPOILER: It's a data flow graph.
"""

"""
=== Poll: recap/review on data flow graphs ===

In the last lecture, we introduced a new tool for visualizing
data processing pipelines called a "dataflow graph".

A dataflow graph has a bunch of "nodes", one node per task
that needs to be completed.
It has arrows between the nodes indicating which tasks are dependent
on each other.

POLL:

The poll gives an example of a dataflow graph and asks
you to identify the 3 types of parallelism in the graph.

https://forms.gle/Vxfw7x5GQgnaetbz9

=== Introduction to distributed programming ===

What is a scalable collection type?

A:

Basic scalable collection types in Spark:

- RDD

- PySpark DataFrame
"""

basic_rdd = sc.parallelize(range(0, 1_000))

"""
What does the above do?

Think of it as...

Q: Why do we need sc. context?

A:
"""

"""
RDD means...
"""

"""
What can we do with our RDD?
"""

"""
A second example: using DataFrame:
"""

# people = spark.createDataFrame([
#     {"deptId": 1, "age": 40, "name": "Hyukjin Kwon", "gender": "M", "salary": 50},
#     {"deptId": 1, "age": 50, "name": "Takuya Ueshin", "gender": "M", "salary": 100},
#     {"deptId": 2, "age": 60, "name": "Xinrong Meng", "gender": "F", "salary": 150},
#     {"deptId": 3, "age": 20, "name": "Haejoon Lee", "gender": "M", "salary": 200}
# ])

# people_filtered = people.filter(people.age > 30)

# people_filtered.show()

# people2 = sc.parallelize([
#     {"deptId": 1, "age": 40, "name": "Hyukjin Kwon", "gender": "M", "salary": 50},
#     {"deptId": 1, "age": 50, "name": "Takuya Ueshin", "gender": "M", "salary": 100},
#     {"deptId": 2, "age": 60, "name": "Xinrong Meng", "gender": "F", "salary": 150},
#     {"deptId": 3, "age": 20, "name": "Haejoon Lee", "gender": "M", "salary": 200}
# ])

# people2_filtered = people2.filter(lambda x: x["age"] > 30)

# result = people2_filtered.collect()

# print(result)

"""
Auto parallelization / auto distribution?

Analogy: Apache Spark is kind of like a compiler.
"""
