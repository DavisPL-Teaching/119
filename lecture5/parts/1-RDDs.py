"""
Lecture 5: Distributed Pipelines

Part 1: Introduction to Spark: Scalable collection types and RDDs

=== Poll ===

Speedup through parallelism alone (vertical scaling) is most significantly limited by...
(Select all that apply)

1. The number of lines in the Python source code
2. The version of the operating system (e.g., MacOS Sonoma)
3. The number of CPU cores on the machine
4. The number of wire connections on the computer's motherboard
5. The amount of RAM (memory) and disk space (storage) available

https://forms.gle/LUsqdy7YYKy7JFVH6

=== Apache Spark (PySpark) ===

In this lecture, we will use Apache Spark (PySpark).

Spark is a parallel and distributed data processing framework.

(Note: Spark also has APIs in several other languages, most typically
Scala and Java. The Python version aligns best with the sorts of
code we have been writing so far and is generally quite accessible.)

Documentation:
https://spark.apache.org/docs/latest/api/python/index.html

To test whether you have PySpark installed successfully, try running
the lecture now:

python3 1-RDDs.py
"""

# Test whether import works
import pyspark

# All spark code generally starts with the following setup code:
# (Boiler plate code - ignore for now)
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
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

We say "what" we want, the distributed data processing software framework will
handle the "how"

So what is that higher level abstraction?

Spoiler:
It's dataflow graphs!

(With one additional thing)
"""

"""
=== Introduction to distributed programming ===

What is a scalable collection type?

What is a collection type? A set, a list, a dictionary, a table,
a DataFrame, a database (for example), any collection of objects, rows,
or data items.

    - Pandas DataFrame is one example.

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

- PySpark DataFrame API
    Will bear resemblance to DataFrames in Pandas (and Dask)
"""

# Uncomment to run
# # RDD - scalable version of a Python set of integers
# basic_rdd = sc.parallelize(range(0, 1_000))

# print(basic_rdd)

# # --- run some commands on the RDD ---
# mapped_rdd = basic_rdd.map(lambda x: x + 2)
# filtered_rdd = mapped_rdd.filter(lambda x: x > 500)
# result = filtered_rdd.collect()

# print(result)

"""
We can visualize our pipeline!

Open up your browser to:
http://localhost:4040/

=== More examples ===

Scalable collection types are just like normal collection types!

Let's show this:

Exercises:
1.
Write a function
a) in Python
b) in PySpark using RDDs
that takes an input list of integers,
and finds only the integers x such that x * x is exactly 3 digits...

- .map
- .filter
- .collect
"""

def ex1_python(l1):
    # anonymous functions with map filter!
    l2 = map(lambda x: x * x, l1)
    # ^^ equivalent to
    # def anon_function_square(x):
    #     return x * x
    # l2 = map(anon_function_square, l1)
    # list comprehension syntax:
    # [x * x for x in l1]
    l3 = filter(lambda x: 100 <= x <= 999, l2)
    print(list(l3))

INPUT_EXAMPLE = list(range(100))

# ex1_python(INPUT_EXAMPLE)

# Output:
# [100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961]
# All the 3 digit square numbers!

def ex1_rdd(list):
    l1 = sc.parallelize(list) # how you construct an RDD
    l2 = l1.map(lambda x: x * x)
    # BTW: equivalent to:
    # def square(x):
    #     return x * x
    # l2 = l1.map(square)
    l3 = l2.filter(lambda x: 100 <= x <= 999)
    print(l3.collect())

# ex1_rdd(INPUT_EXAMPLE)

"""
2.
Write a function
a) in Python
b) in PySpark using RDDs
that takes as input a list of integers,
and adds up all the even integers and all the odd integers

- .groupBy
- .reduceBy
- .reduceByKey
- .partitionBy
"""

def ex2_python(l1):
    # (Skip: leave as exercise)
    # TODO
    raise NotImplementedError

def ex2_rdd(l1):
    l2 = sc.parallelize(l1)
    l3 = l2.groupBy(lambda x: x % 2)
    l4 = l3.flatMapValues(lambda x: x)
    # ^^ needed for technical reasons
    # actually, would be easier just to run a map to (x % 2, x)
    # then call reduceByKey, but I wanted to conceptually separate
    # out the groupBy step from the sum step.
    l5 = l4.reduceByKey(lambda x, y: x + y)
    for key, val in l5.collect():
        print(f"{key}: {val}")
    # Uncomment to inspect l1, l2, l3, l4, and l5
    # breakpoint()

# ex2_rdd(INPUT_EXAMPLE)

"""
Good! But there's one thing left -- we haven't really measured
that our pipeline is actually getting run in parallel.

Q: Can we check that?

    Test: parallel_test.py

A: Tools:

    time (doesn't work)

    Activity monitor

    localhost:4040
    (see Executors tab)

Q: what is localhost? What is going on behind the scenes?

A: Spark is running a local cluster on our machine to schedule and run
   tasks (batch jobs).

Q: Why do we need sc.context?

A:
Not locally using Python compute, so any operation we do
needs to get submitted and run as a job through the cluster.

Q: What does RDD stand for?

RDD means Resilient Distributed Dataset.
https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf

=== That's Just Data Parallelism! (TM) ===

Yes, the following is a punchline:

    scalable collection type == data parallelism.

They are really the same thing.

Task, pipeline parallelism are limited by the # of nodes in the graph!
Data parallelism = arbitrary scaling, so it's what enables scalable
collectiont types.

Brings us to: how can we tell from looking at a dataflow graph if it can
be parallelized and distributed automatically in a framework like PySpark?

    A: All tasks must be data-parallel.

=== Summary ===

We saw scalable collection types
(with some initial RDD examples)

Scalable collection types are just like normal collection types,
but they behave (behind the scenes) like they work in parallel!

They do this by automatically exploiting data parallelism.

Behind the scenes, both vertical scaling and horizontal scaling
can be performed automatically by the underlying data processing
engine (in our case, Spark).

This depends on the engine to do its job well -- for the most part,
we will assume in this class that the engine does a better job than
we do, but we will get to some limitations later on.

Many other data processing engines exist...
(to name a few, Hadoop, Google Cloud Dataflow, Materialize, Storm, Flink)
(we will discuss more later on and the technology behind these.)

=== Plan for remaining parts ===

Overall plan for Lecture 5:

- Scalable collection types

- Programming over collection types

- Important properties: immutability, laziness

- MapReduce

    Simpler abstraction underlying RDDs and Spark

- Partitioning in RDDs and collection types

Possible topics/optional:

- Distributed consistency: crashes, failures, duplicated/dropped/reorder messages

- Pitfalls.
"""
