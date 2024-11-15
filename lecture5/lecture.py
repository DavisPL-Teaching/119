"""
Lecture 5: Distributed Pipelines

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

********** Ended here for Nov 4 **********

==========================================

=== Nov 6 ===

=== Poll ===

Speedup through parallelism alone (vertical scaling) is significantly limited by...
(Select all that apply)

1. The number of lines in the Python source code
2. The version of the operating system (e.g., MacOS Sonoma)
3. The number of CPU cores on the machine
4. The number of wire connections on the computer's motherboard
5. The amount of RAM (memory) and disk space (storage) available

https://forms.gle/fqLbb9dw7w96wVkR9

=== Recap ===

Scalable collection types are just like normal collection types,
but they behave (behind the scenes) like they work in parallel!

Behind the scenes, both vertical scaling and horizontal scaling
can be performed automatically by the underlying data processing
engine (in our case, Spark).
This depends on the engine to do its job well -- for the most part,
we will assume in this class that the engine does a better job than
we do, but we will get to some limitations later on.

Many other data processing engines exist...
(to name a few, Hadoop, Google Cloud Dataflow, Materialize, Storm, Flink)
(we will discuss more later on and the technology behind these.)

I said:
    "scalable collection types are just like normal collection types"

Let's show this!

Exercise:
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
    l2 = map(lambda x: x * x, l1)
    l3 = filter(lambda x: 100 <= x <= 999, l2)
    print(list(l3))

INPUT_EXAMPLE = list(range(100))

# ex1_python(INPUT_EXAMPLE)

# Output:
# [100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961]
# All the 3 digit square numbers!

def ex1_rdd(list):
    l1 = sc.parallelize(list)
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

Can we check that?

    Test: parallel_test.py

Tools:

    time (doesn't work)

    Activity monitor

    localhost:4040
    (see Executors tab)

Q: what is localhost? What is going on behind the scenes?

A: Spark is running a local cluster on our machine to schedule and run
   tasks (batch jobs).


Q: Why do we need sc. context?

A:
Not locally using Python compute, so any operation we do
needs to get submitted and run as a job through the cluster.

Q: What is an RDD?

RDD means Resilient Distributed Dataset.
https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf

Important properties of RDDs:

- Scalability (we have already discussed this)

- Fault tolerance
    RDD data will actually automatically recover if a node (worker or machine) crashes
    It does this while still mostly maintaining data in-memory, which is impressive.

- Immutability

Let's illustrate this:

Exercise: try this:
- Create an RDD
- Collect
- Modify the result
What happens?

(It doesn't work)

RDDs are optimized for computing static, immutable results.
"""

"""
- Laziness

=== Laziness ===

What is laziness?

--> Spark will delay computing answers until you ask for them, as much
    as possible.
    (Dask does the same thing -- we saw a very brief example)

You might wonder: why not just compute all the answers up front?

Conjectures?
- If you're pipelining the output, you could save memory!
  (operator1) --> (operator2)
  Doing operator1, then operator2 is ineficient (lots of stuff stored in memory)
  (and we didn't anything in parallel)
  Doing them both at once allows Spark to optimize the pair of them together.

- More generally: we want to optimize the pipeline before running it.

Recap:

- We saw RDDs, properties of RDDs: parallelism, laziness, partitioning.
- We'll go into these more next time (next Wed) and talk about the DataFrame
  API as well.

***** Stopped here for Nov 6 *****

====================================

Friday, Nov 15

=== Poll ===

Review question about RDDs:

https://forms.gle/fPL8cyBMhTkR4MQUA

=== Recap ===

Properties of scalable colleciton types:

    RDDs are: scalable, parallel, immutable, lazy, and partitioned.

    Operators on RDDs create dataflow graphs! (more on this soon)

    We have covered the first 3 properties so far and briefly mentioned the 4th one.

Not just about RDDs!

---> Most of this generalizes to all distributed programming contexts.

=== Laziness ===

In Spark, and in particular on RDDs,
operators are divided into *transformations* and *actions.*

https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html

Transformation: transform the data without computing the answer (yet)
Action: compute an answer

This is called "laziness" because we don't always compute the answer right away.

Terminology (this comes from programming language design):
Transformations are also called "lazy" operators
and actions are called "eager" operators.
(Why?)

Let's consider an example

A chemical dataset:
"""

# Chem names by atomic number
CHEM_NAMES = [None, "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"]
CHEM_DATA = {
    # H20
    "water": [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    # N2
    "nitrogen": [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    # CO2
    "carbon dioxide": [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0],
    # C4H
    "methane": [0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    # C8 H F15 O2
    "PFOA": [0, 1, 0, 0, 0, 0, 8, 0, 2, 15, 0],
}

# Example: we want to find molecules that are heavy in Fluorine (F)
# Note:
# More about PFOA:
# https://en.wikipedia.org/wiki/Perfluorooctanoic_acid#Health_effects
# Dark Waters (2019 film)
# https://en.wikipedia.org/wiki/Dark_Waters_(2019_film)

def fluorine_carbon_ratio(data):
    # Note: a nice thing in Spark is that we can parallelize any iterable collection!
    # (We should really use a DataFrame for this, I just want to show RDDs as we have been using
    # RDD syntax so far. DataFrames are based on RDDs under the hood.)
    rdd1 = sc.parallelize(data.values())

    # We can't compute the ratio if there are no carbons
    rdd2 = rdd1.filter(lambda x: x[6] > 0)

    # Compute ratio
    rdd3 = rdd2.map(lambda x: x[9] / x[6])

    # Compute avg
    stats = rdd3.stats()
    ans = stats.mean()

    # Print
    print(f"Stats: {stats}")
    print(f"Average Fluorine-Carbon Ratio: {ans}")

# Comment out to run
# fluorine_carbon_ratio(CHEM_DATA)

"""
How can we determine which of the above are lazy (transformations) and which are eager (actions)?

Ideas?

Answers:

Lazy (transformations):

-

Eager (actions):

-
"""

"""
=== Interlude: RDDs as dataflow graphs ===

Before we continue: viewing the above as a dataflow graph!

All distributed pipelines can be viewed as dataflow graphs. How?

Q: let's draw the above as a dataflow graph using ASCII art.

(What are our tasks/nodes and arrows?)

"""

"""
Can we view this more programmatically?

Unfortunately the visualization capabilities of RDDs are a bit limited.
Two ways for now:

- Go to localhost:4040/
- .toDebugString()

We will see a better way when we get to DataFrames.
"""

"""
=== More examples of laziness ===

More examples of transformations are:

- .map
- .filter
- .sample(withReplacement, fraction)
- .distinct()

Some examples of actions are:

- .collect
- .count()
- .sum()
- .reduce()
- .fold()
- .flatMap()
"""

# Try this (in the above function):
# rdd3.distinct().collect()

"""
=== Partitioning ===

Partitioning is what makes RDDs scalable.
How does partitioning work?

----> Under the hood, all datasets and intermediate outputs are partitioned
into groups which can be processed independently.

Useful operations to see what's going on:

    .getNumPartitions
    .glom().collect()

Let's see an example.
"""

def show_partitions(data):

    # Parallelize as before
    rdd = sc.parallelize(data.values())

    # Show the partitioning details
    print(f"Number of partitions: {rdd.getNumPartitions()}")
    print(f"Inspect partitions: {rdd.glom().collect()}")

"""
We can also control the number of partitions and the way data is partitioned
(if we so choose).
"""

def set_partitions(data):

    # Parallelize as before
    rdd = sc.parallelize(data.values())

    # Show the partitioning details
    print(f"Number of partitions: {rdd.getNumPartitions()}")
    print(f"Inspect partitions: {rdd.glom().collect()}")

"""
=== Why partitioning matters ===

We said that scalable collections should behave just like ordinary collections!
So why do we need to worry about partitioning?

----> Sometimes you want to control partitiononing, or partitioning differently helps improve
      the performance of your pipeline.

----> Also occasionally (usually if you set up your pipeline wrong), partitioning might affect the
      outputs that you get.

Q: How does partitioning affect pipeline scheduling and performance?

Like laziness, partitioning also introduces an interesting dichotomy of operators into two groups.

The basic question is what happens when we chain together two operators?

EXAMPLE:
Dataflow graph:

    (input data) ---> (filter) ---> (map) ---> (stats)

What happens when we parallelize this?

A:


Two types of operators!

In addition to being divided into actions and transformations,
RDD operations are divided into "narrow" operations and "wide" operations.

Image:

    narrow_wide.png
    (Credit: LinkedIn)

Definitions:

    Narrow = ...

    Wide = ...

Let's use the definitions above to classify all the operations in our example pipelines above
into narrow and wide.

Narrow:
-

Wide:
-
"""

"""
=== Other interesting operations ===
(Likely skip for time)

Implementation and optimization details:

(See PySpark documentation)

- .id()
- .coalesce()
- .barrier()
- .cache()
- .persist()
- .checkpoint()
"""

"""
=== DataFrame ===

Our second example of a collection type is DataFrame.

DataFrame is kind of like a Pandas DataFrame.

https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html

An example of a dataframe computation is shown in

    examples.py

The main difference is we need to create the dataframe using a tuple or dictionary.

We can also create one from an RDD by doing

    .map(lambda x: (x,)).toDF()
"""

def ex_dataframe(data):
    # TODO:
    # Load the CHEM_DATA and turn it into a DataFrame, then collect it
    raise NotImplementedError

"""
Another misc. DataFrame example:
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
What is the "magic" behind how Spark works?

=== MapReduce ===

MapReduce is a simplified way to implement and think about
distributed pipelines.

In fact, a MapReduce pipeline is the simplest possible pipeline
you can create, with just two stages!

Exercise: Let's create our own MapReduce pipeline functions.
"""

def map(rdd, f):
    # TODO
    raise NotImplementedError

def reduce(rdd, init, f):
    # TODO
    raise NotImplementedError

# If done correctly, the following should work

def get_total_fluorines(data):
    rdd = sc.parallelize(data.values())

    res1 = map(rdd, lambda x: x[9])
    res2 = reduce(res1, 0, lambda x, y: x + y)

    print(f"Result: {res2}")

# Uncomment to run
# get_total_fluorines(CHEM_DATA)

"""
=== Some history ===

MapReduce was originally created by
Jeffrey Dean and Sanjay Ghemawat at Google to simplify the large-scale data processing jobs that
engineers were running on Google clusters.

Blog article: "The Friendship That Made Google Huge"
"Coding together at the same computer, Jeff Dean and Sanjay Ghemawat changed the course of the company—and the Internet."
https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge

One of the paper readings from Wednesday asked you to read the original paper:
    MapReduce: Simplified Data Processing on Large Clusters
    https://dl.acm.org/doi/pdf/10.1145/1327452.1327492

(BTW, this paper is very famous. Probably one of the most cited papers ever with
23,309 citations (last I checked))

Spark is heavily based on MapReduce under the hood.

=== End note: Latency/throughput tradeoff ===

So, we know how to build distributed pipelines.

The **only** change from a sequential pipline is that
arrows are scalable collection types, instead of regular data types.
Tasks are then interpreted as (either wide or narrow) operators over the scalable collections.
In other words, data parallelism comes by default and for free!

But there is just one problem with what we have so far :)
Spark is optimized for throughput.
It's what we call a *batch processing engine.* That means?

This is related to the last question on Q10 of the midterm.
It wasn't entirely clear to everyone what I meant by latency on a "single input"
vs. the "entire input dataset", so let me clarify.

First of all, what is latency?
Imagine this. I have 10M inputs, my pipeline processes 1M inputs/sec (pretty well parallelized.

    (input)   --- (process)
      10M        1M / sec

What's the latency if I just put 1 item into the pipeline?

If I make some change to the input, how long will it take to see the results on the
output side?

We can't say from the above information. We don't know for example, whether the
1M inputs/sec means all 1M are processed in parallel, or the 1M inputs/sec means that
it's really 100K inputs every tenth of a second at a time.

**Latency is about response time.**
To understand latency you have to imagine the data is coming in to the pipeline in real time,
hot off the press.

It only makes sense to talk about latency when we're thinking about an input change that the user
makes (some input data), and the result they want to observe on the output side.
Latency is always measured in seconds; it's not a time "per item" or dividing the total time by number
of items (that doesn't tell us how long it took to see a response for each individual item!)

But in a batch processing framework like Spark,
it waits until we ask, and then collects *all* results at once!
So we always get the worst possible throughput, in fact we get 10 seconds latency
on each individual item. We don't get some results sooner and some results later.

Grouping together items (via lazy transformations) helps optimize the pipeline, but it
*doesn't* help get results as soon as possible when they're needed. That's why there is a tradeoff
between throughput and latency.
If we always wanted the best latency, we would only ever do actions, never transformations,
and we would always ask for the results right away.

From "The 8 Requirements of Real-Time Stream Processing":

    "To achieve low latency, a system must be able to perform
    message processing without having a costly storage operation in
    the critical processing path. A storage operation adds a great deal
    of unnecessary latency to the process (e.g., committing a database
    record requires a disk write of a log record). For many stream
    processing applications, it is neither acceptable nor necessary to
    require such a time-intensive operation before message processing
    can occur. Instead, messages should be processed “in-stream” as
    they fly by."

    Mike Stonebraker, Ugur Çetintemel, and Stan Zdonik
    https://cs.brown.edu/~ugur/8rulesSigRec.pdf

So that's where we're going next,
talking about applications where you might want your pipeline to respond in real time to data that
is coming in.
We'll use a different API in Spark called Spark Streaming.
"""
