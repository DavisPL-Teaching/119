"""
Lecture 5: Distributed Pipelines

Part 1: Scalable collection types and RDDs

----

Agenda:

- Recap: on dataflow graphs

- Scalable collection types

- Programming over collection types

Possible topics/optional:

- Throughput and latency model

- Partitioning strategies

- Distributed consistency: crashes, failures, duplicated/dropped messages

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

    + e.g.: I have 800 GB available, but if I want to work with a dataset
      bigger than that, I'm out of luck

    + e.g.: I have 16 CPU cores available, but if I want more than 16X
      speedup, I'm out of luck

We want to be able to scale pipelines automatically to larger datasets.
How?

Idea:

- **Build our pipelines** at a higher level of abstraction -- build data sets and operators over data sets

- **Deploy our pipelines** using a framework or library that will automatically scale and take advantage of parallel and distributed compute resources.

Analogy: kind of like a compiler or interpreter!
    (A long time ago, people use to write all code in assembly language/
    machine code)

We say "what" we want, the distriuted data processing software framework will
handle the "how"

So what is that higher level abstraction?

SPOILER: It's a dataflow graph.
"""

# Recall: distributed pipeline from previous lecture below:

# for os.popen to run a shell command (like we did on HW1 part 3)
import os

def ssh_run_command(cmd):
    result = os.popen("ssh cdstanfo@set.cs.ucdavis.edu " + cmd).read()
    # Just print the result for now
    print(f"result: {result.strip()}")

def worker1_distributed():
    ssh_run_command("seq 1 1000000 | awk '{s+=$1} END {print s}'")
    print("Worker 1 finished")

def worker2_distributed():
    ssh_run_command("seq 1000001 2000000 | awk '{s+=$1} END {print s}'")
    print("Worker 2 finished")

def average_numbers_distributed():
    worker1_distributed()
    worker2_distributed()
    print("Distributed computation complete")

# Uncomment to run
# This won't work on your machine!
# average_numbers_distributed()

"""
=== Introduction to distributed programming ===

What is a scalable collection type?

What is a collection type? A set, a list, a dictionary, a table,
a DataFrame, a database (for example), any collection of objects, rows,
or data items.

When we talk about collection types, we usually assume the whole
thing is stored in memory. (Refer to 800GB limit comment above.)

A: "Scalable" part means the collection is automatically distributed
and parallelized over many different workers and/or computers or devices.

The magic of this is that we can think of it just like a standard
collection type!

If I have a scalable set, I can just think of that as a set

If I have a scalable DataFrame, I can just think of that as a DataFrame

Basic scalable collection types in Spark:

- RDD
    Resilient Distributed Dataset

- PySpark DataFrame APi
    Will bear resemblance to DataFrames in Pandas (and Dask)
"""

basic_rdd = sc.parallelize(range(0, 1_000))

# --- run some commands on the RDD ---
# mapped_rdd = basic_rdd.map(lambda x: x + 2)
# filtered_rdd = mapped_rdd.filter(lambda x: x > 500)
# filtered_rdd.collect()

"""
We can visualize our pipeline!

Open up your browser to:
http://localhost:4040/

Let's wrap up there:

- We saw scalable collection types
  (with an initial RDD example)

  And we will do more examples next time.
"""
