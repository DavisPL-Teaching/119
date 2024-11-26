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

=== Recap ===

Properties of scalable colleciton types:

    RDDs are: scalable, parallel, immutable, lazy, and partitioned.

    Operators on RDDs create dataflow graphs! (more on this soon)

    We have covered the first 3 properties so far and briefly mentioned the 4th one.

Not just about RDDs!

---> Most of this generalizes to all distributed programming contexts.

=== Poll ===

Review question about RDDs:

https://forms.gle/fPL8cyBMhTkR4MQUA

Answers: Vertical + Horizontal scaling, data parallelism, distribution, and should behave
   as if it were a normal collection type

Takeaway message: Scalable collection types == data parallelism!

=== Laziness ===

In Spark, and in particular on RDDs,
operators are divided into *transformations* and *actions.*

https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html

Transformation: transform the data without computing the answer (yet)
Action: compute an answer

This is called "laziness" because we don't always compute the answer right away.

Terminology (this comes from programming language design):
    (e.g. Haskell is lazy)
Transformations are also called "lazy" operators
and actions are called "eager" operators.
(Why?)

Let's consider an example

A toy chemical dataset:
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
    # CH4
    "methane": [0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    # C8 H F15 O2
    "PFOA": [0, 1, 0, 0, 0, 0, 8, 0, 2, 15, 0],
}

"""
Motivation for this example:
Suppose we want to find chemicals that are heavy in Fluorine (F),
because we are worried these might have negative health effects.

Further reading:
Dark Waters (2019 film)
https://en.wikipedia.org/wiki/Dark_Waters_(2019_film)
PFOA:
https://en.wikipedia.org/wiki/Perfluorooctanoic_acid#Health_effects

For a simple computation, let's try to compute the number of Fluorines,
compared to the number of Carbons for all of our data points,
and then compute an average.
"""

def fluorine_carbon_ratio(data):
    # Note: a nice thing in Spark is that we can parallelize any iterable collection!
    # (We should really use a DataFrame for this, I just want to show RDDs as we have been using
    # RDD syntax so far. DataFrames are based on RDDs under the hood.)
    rdd1 = sc.parallelize(data.values())
    # .keys() gives water, nitrogen, etc.
    # .values() gives the lists [0, 1, ...]
    # .items() to get the (name, list) pair

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

    # Uncomment to debug
    # breakpoint()

# Uncomment to run
# fluorine_carbon_ratio(CHEM_DATA)

"""
How can we determine which of the above are transformations and which are actions?

Ideas?

- Print it out!

  Transformation = prints out as an RDD (it's just a blob that doesn't have any data output)

    After a transformation: PythonRDD[3] at RDD at PythonRDD.scala:53

  Action = prints out as Python data.

    After an action: (count: 3, mean: 0.625, stdev: 0.8838834764831844, max: 1.875, min: 0.0)

Answers:

Transformations (lazy):

- .map(), .filter()

Actions (not lazy):

- .stats()
"""

"""
=== Interlude: RDDs as dataflow graphs ===

Before we continue: viewing the above as a dataflow graph!

All distributed pipelines can be viewed as dataflow graphs. How?

What is the connection between code and dataflow graphs?

Q: let's draw the above as a dataflow graph using ASCII art.

(What are our tasks/nodes and arrows?)

    Tasks: Operators that were done on the RDD
    Arrows: dependencies from one operator to another

    Our dataflow graph:

    (input chem data) --> (filter) --> (map) --> (stats)

    Each task computes a new RDD based on the old RDD.

    Calling an operator/method .do_something on an RDD creates a new node (do_something)

    This:
    rdd = sc.parallelize(...)
    rdd1 = rdd.operator1()
    rdd2 = rdd.operator2()
    rdd3 = rdd2.operator3()

    Is the same as

    This:
                --> (operator1)
    (load input)
                --> (operator2) --> (operator3)

(In fact, underneath the hood, PySpark is actually creating the dataflow graph.)
"""

"""
Can we view this more programmatically?

Unfortunately the visualization capabilities of RDDs are a bit limited.
Two ways for now:
Both of these are not super helpful and don't give precise information.

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

The most important of these is .collect -- how to take any RDD and get the results.
You can that at any intermediate stage.
"""

# Try this (in the above function):
# rdd3.distinct().collect()

"""
=== Wrapping up ===

We saw
    scalable collection type == data parallelism.

We saw Laziness of RDDs: all RDD operators are divided into transformations
(which return another RDD object/handle and don't compute anything)
and actions (which return result data in plain Python)

We saw that all computations over RDDs are really dataflow graphs.
    code == dataflow graph

**************** Where we left off for today ****************

=============================================================

=== Nov 18 ===

=== Poll ===

https://forms.gle/bfhtG8WqiYcco72e7

An exercise on laziness:

Suppose we want to do 3 tasks:

1. Generate 100,000 random data points (vectors v)
2. Map each data point v to a normalized vector v / ||v||
3. Print the first 5 answers

As a dataflow graph:
(1) ---> (2) ---> (3)

We want to know which of 1, 2, 3 should be lazy, and which should be evaluated right away.

Which tasks should be evaluated lazily if we want to get the answer in the most efficient way?

(Note: we will revisit this example again soon.)

=== Finishing up RDDs ===

One last property (an important one!): Partitioning

=== Partitioning ===

Whenever we consruct an RDD, under the hood it is going to be partitioned
into several chunks or subsets of the data; these could be all stored on the same machine,
or they could be stored on separate distributed machines.

Partitioning is what makes RDDs a scalable collection type.
It's data parallelism.

How does partitioning work?

----> Under the hood, all datasets and intermediate outputs are partitioned
      into groups which can be processed independently.

Useful operations to see what's going on:

    .getNumPartitions
    .glom().collect()

Let's revisit our example:
"""

def show_partitions(data, num_partitions=None):

    # Parallelize as before
    if num_partitions is None:
        rdd = sc.parallelize(data.values())
    else:
        rdd = sc.parallelize(data.values(), num_partitions)

    # Show the partitioning details
    print(f"Number of partitions: {rdd.getNumPartitions()}")
    print("Inspect partitions:")
    for part in rdd.glom().collect():
        # What glom does: it takes each partition for example partition 1, 2, 3, 4, 5
        # And it effectively adds a coordinate to each input data item that indicates the partition #.
        # After we do a glom we can do a collect and then explicitly iterate through the partitions.

        # In short: It allows to view the partitions.

        # Print the partition
        print(f"Partition: {part}")

# Uncomment to run
# show_partitions(CHEM_DATA)

"""
What numbers did we get?
- I got 12 -- my machine has 12 cores

Other people got?
- 8

In this case, all partitions are on the same machine (my laptop),
but in general they could be split accross several machines.
"""

"""
We can also control the number of partitions and the way data is partitioned
(if we so choose).
Syntax:

     sc.parallelize(data, number of partitions)
"""

# Exercise: update the above to also control the number of partitions as an optional
# parameter, then print
# show_partitions(CHEM_DATA, 1)
# show_partitions(CHEM_DATA, 5)
# show_partitions(CHEM_DATA, 10)

"""
So far: we know (1) how to inspect the partitions (2) how to change the number of partitions.

=== Why partitioning matters! ===

We said that scalable collections should behave just like ordinary collections!
So why do we need to worry about partitioning?

----> No abstraction is perfect! Sometimes we need further control over the pipeline
      to improve performance.

Anecdote:
A friend of mine who worked as a data/ML engineer told me the following story:
(from my notes):

    2 hours to look at the first 10 rows of a table in dataproc!

    turned out there was a formula to calculate the size of the partitions --
    5 rows in each partition, 1 billion partitions.

    spent a day optimizing this and then it took 1 minute to do the same thing!

(Dataproc is Google Cloud's framework for running Spark and other distributed
data processing tasks: https://cloud.google.com/dataproc)

Moral of the story:
In an ideal world, we wouldn't worry about partitioning,
if the number of partitions created is wildly off from the
size of the data set (too small or too large), it could have severe impacts
on performance.

----> Side note: Even worse, partitioning might affect the
      outputs that you get. This shouldn't happen unless you wrote your pipeline
      incorrectly (but happy to talk more about this if there is time in a lecture
      at some point!).

Review Q:
Why does partitioning affect pipeline scheduling and performance?

A:
It controls the amount of data parallelism in the pipeline
Too little data parallelism, and we don't benefit from parallelism
Too much, and we might have severe/large overheads from creating and managing all the partitions.

=== Two types of operators (again) ===

Like laziness, partitioning also introduces an interesting dichotomy of operators into two groups.

The basic question is what happens when we chain together two operators?

EXAMPLE:
Dataflow graph:

    (load input data) ---> (filter) ---> (map) ---> (stats)

Q:
Suppose there are two partitions for each task.
If we draw one node per partition, instead of one node per task,
what dataflow graph would we get?

A (class input):

    (load input data, 1st half) ---> (filter, 1st half) ---> (map, 1st half)
                                                                             ----->
                                                                                    (stats)
                                                                             ----->
    (load input data, 2nd half) ---> (filter, 2nd half) ---> (map, 2nd half)

(Data parallelism, previously implicit, has now been explicitly represented as task parallelism.)

(This process is what Spark does underneath the hood:
    automatically parallelizing, or "autoparallelizing" the input graph.)

The two types of operators are revealed!

In addition to being divided into actions and transformations,
RDD operations are divided into "narrow" operations and "wide" operations.

Definitions:

    Narrow = works on individual partitions only

    Wide = works across partitions.

Image:

    narrow_wide.png
    (Credit: LinkedIn)

We saw partitioning and that it gives rise to narrow/wide operators,
and what it does to the input data flow graph.

We'll pick this up on Wednesday.

========================================================

=== Wed Nov 20 ===

=== Poll ===

Consider the following scenario where a temperature dataset is partitioned in Spark across several locations. Which of the following tasks on the input dataset could be done with a narrow operator, and which would require a wide operator?

https://forms.gle/bex7HBzRSd6824TM9

=== Finishing up narrow and wide ===

Let's use the definitions above to classify all the operations in our example pipelines above
into narrow and wide.

Narrow:
- map
- filter

Wide:
- total avg
- total count
- stddev
- etc.
- globally unique / distinct elements
- anything where you need to communicate across partitions.

"""

"""
=== Other miscellaneous interesting operations ===
(Likely skip for time)

Implementation and optimization details:
(See PySpark documentation)

- .id()
- .coalesce()
- .barrier()
- .cache()
- .persist()
- .checkpoint()

These can be more important if you are worried about performance,
or crashes/failures and other distributed concerns.
"""

"""
=== MapReduce and DataFrames ===

DataFrames are based on RDDs and RDDs are based on MapReduce!
A little picture:

  DataFrames
  |
  RDDs
  |
  MapReduce

=== DataFrame ===

(Will probably skip some of this for time)

Our second example of a collection type is DataFrame.

DataFrame is like a Pandas DataFrame.

https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html

An example of a dataframe computation is shown in

    examples.py

The main difference is we need to create the dataframe using a tuple or dictionary.

We can also create one from an RDD by doing

    .map(lambda x: (x,)).toDF()
"""

def ex_dataframe(data):
    # Load the data (CHEM_DATA) and turn it into a DataFrame

    # A few ways to do this

    """
    Method 1: directly from the RDD
    """
    rdd = sc.parallelize(data.values())

    # RDD is just a collection of items where the items can have any Python type
    # a DataFrame requires the items to be rows.

    df1 = rdd.map(lambda x: (x,)).toDF()

    # Breakpoint for inspection
    # breakpoint()

    # Try: df1.show()

    # What happened?

    # Not very useful! Let's try a different way.
    # Our lambda x: (x,) map looks a bit sus. Does anyone see why?

    """
    Method 2: unpack the data into a row more appropriately by constructing the row
    """
    # don't need to do the same thing again -- RDDs are persistent and immutable!
    # rdd = sc.parallelize(data.values())

    # In Python you can unwrap an entire list as a tuple by using *x.
    df2 = rdd.map(lambda x: (*x,)).toDF()

    # Breakpoint for inspection
    # breakpoint()

    # What happened?

    # Better!

    """
    Method 3: create the DataFrame directly with column headers
    (the correct way)
    """

    # What we need (similar to Pandas): list of columns, iterable of rows.

    # For the columns, use our CHEM_NAMES list
    columns = ["chemical"] + CHEM_NAMES[1:]

    # For the rows: any iterable -- i.e. any sequence -- of rows
    # For the rows: can use [] or a generator expression ()
    rows = ((name, *(counts[1:])) for name, counts in CHEM_DATA.items())

    # Equiv:
    # rows = [(name, *(counts[1:])) for name, counts in CHEM_DATA.items()]
    # Also equiv:
    # for name, counts in CHEM_DATA.items():
    #     ...

    df3 = spark.createDataFrame(rows, columns)

    # Breakpoint for inspection
    # breakpoint()

    # What happened?

    # Now we don't have to worry about RDDs at all. We can use all our favorite DataFrame
    # abstractions and manipulate directly using SQL operations.

    # Adding a new column:
    from pyspark.sql.functions import col
    df4 = df3.withColumn("H + C", col("H") + col("C"))
    df4 = df3.withColumn("H + F", col("H") + col("F"))

    # This is the equiv of Pandas: df3["H + C"] = df3["H"] + df3["C"]

    breakpoint()

    # We could continue this example further (showing other Pandas operation equivalents).

# Uncomment to run
# ex_dataframe(CHEM_DATA)

"""
One more thing about DataFrames: revisiting the web interface
and .explain():

localhost:4040/

getting the internal dataflow graph used:

.explain()

.explain("extended")
"""

"""
Another misc. DataFrame example:
(skip for time, feel free to uncomment and play with it offline)
"""

# Just to show how to create a data frame from a Python dict.

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
So we know how to work with DataFrames, once we do that, we don't have to worry about RDDs
at all. We get nice SQL abstractions.

What is the "magic" behind how Spark works?

=== MapReduce ===

MapReduce is a simplified way to implement and think about
distributed pipelines.

MapReduce tries to take all distributed data pipelines you might want to
compute, and reduce them down to the bear essence of the very minimal
number of possible operations.

In fact, a MapReduce pipeline is the simplest possible pipeline
you can create, with just two stages!
It's a dataflow graph with just three nodes:

    (input) ---> (map) ---> (reduce).

The kind of amazing thing is that essentially all operators on distributed
pipelines can be reduced down to this simple form,
called a MapReduce job.
(Sometimes you might you need more than one MapReduce job to get some computations
done.)

(Simplified)

Map stage:
    - Take our input a scalable collection of items of type T, and apply
      the same function f: T -> T to all inputs.

      (T could be, integers, floats, chemicals, rows, anything)

Reduce stage:
(This differs a little by implementation)
    - a way of combining two different intermediate outputs:
      a function f: T x T -> T.

Example:

    My input dataset consists of populations by city.
    I want the total population over all cities.

    If I wanted to do this as MapReduce:

    Map: do nothing, on each input row x, return x
        lambda x: x

        If input x was a row insetad of a integer, you could do
        lambda x: x["population"]

    Reduce: if I have two outputs x and y, return x + y
        lambda x, y: x + y.

    The MapReduce computation will repeatedly apply the reduce function
    until there is no more reducing to do.

This is only very slightly simplified. Two things to make it general:
(We don't need to cover this for the purposes of this class)

1) it's not all the same type T (input, intermediate, and output stages)
(in fact, intermediate stage can be a list of zero or more outputs, not just one)

2) both stages are partitioned by key.
    + for map, this doesn't matter!
    + for reduce, we actually get one output per key.

Punchline:
In fact we have been writing MapReduce pipelines all along!
See our original CHEM_DATA example:
- map stage: we apply a local computation to each input row: in our case,
  we wanted to get the number of fluorines / num carbons for all rows which
  have at least one carbon.
- reduce stage: we aggregate all outputs across input rows: in our case,
  we wanted to compute the avg across all inputs.

All operators fit into this dichotomy:
- Mapper-style operators are local, can be narrow, and can be lazy
- Reducer-style operators are global, usually wide, and not lazy.

We'll pick this up and finish up the lecture on Friday.

********** Ended here for Nov 20 **********

==================================================

=== Nov 22 ===

=== MapReduce Recap ===

In MapReduce there are only two operators,
Map and Reduce.

PySpark equivalents:
- .map
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.map.html
- .reduce
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.reduce.html#pyspark.RDD.reduce

As we mentioned last time, this is slightly simplified.
We will do the fully general case today!

Also equivalent to reduce (but needs an initial value)
- .fold
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.fold.html
"""

# Re-defining from earlier in the file
# (and adding a couple more molecules)
CHEM_DATA_2 = {
    # H20
    "water": [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    # N2
    "nitrogen": [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    # O2
    "oxygen": [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    # F2
    "fluorine": [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    # CO2
    "carbon dioxide": [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0],
    # CH4
    "methane": [0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    # C2 H6
    "ethane": [0, 6, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    # C8 H F15 O2
    "PFOA": [0, 1, 0, 0, 0, 0, 8, 0, 2, 15, 0],
    # C H3 F
    "Fluoromethane": [0, 3, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    # C6 F6
    "Hexafluorobenzene": [0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0],
}

def map(rdd, f):
    """
    rdd: RDD where the items have type v1
    f: a function v1 -> v2
    output: RDD where the items have type v2

    Apply the f to each input item
    """
    rdd2 = rdd.map(f)

    # Uncomment to show intermediate stage
    print(f"Intermediate: {rdd2.collect()}")

    return rdd2

def reduce(rdd, f):
    """
    rdd: RDD where the items have type v2
    f: v2 x v2 -> v2
       (v2, v2) -> v2
    output: a single value v2

    Apply the f to pairs of values until there's only one left.
    """

    return rdd.reduce(f)

# If done correctly, the following should work

def get_total_hydrogens(data):
    rdd = sc.parallelize(data.values())

    # list x, x[1] gives us the Hydrogen coordinate
    # v1 = list[integers]
    # v2 = integer
    # f: list[integers] -> integer
    res1 = map(rdd, lambda x: x[1])

    # reduce should just add together integers
    # v2 = integer
    # f: (integer, integer) -> integer
    res2 = reduce(res1, lambda x, y: x + y)

    print(f"Result: {res2}")

# Uncomment to run
# get_total_hydrogens(CHEM_DATA_2)
# (Count by hand to check)
# 16 :checkmark:

# Note:
# We could also .collect() and then .parallelize() the results after the
# map stage if we wanted to simulate completing the results of the Map stage
# and reshuffling prior to getting to the Reduce stage.
# Many MapReduce implementations work this way.

"""
=== Poll ===

Describe how you might do the following task as a MapReduce computation.

Same input dataset as in Nov 20 poll:
US state, city name, population, avg temperature

"Find the city with the largest temperature per unit population"

https://forms.gle/Wm1ieauEdgJhiYhD7

Map stage:
(For each row, output ...)

- divide the temperature by the population
- add a new column, save the new value in a new column

What are the types?
Map: for each item of type v1, output an item of type v2
v1 = (state, city name, population, avg temperature)

- v2 = (temperature / population)
- v2 = (state, city name, population, avg temp, temperature / population)

Minimal info we need:
- v2 = (city name, temp / population)

Pseudocode:
f((state, city name, population, avg temperature)):
    return (city name, temp / population)

Reduce stage:
(For each pair of results r1 and r2, combine them to get ...)

- (v2, v2) -> v2
- (city name 1, ratio 1), (city name 2, ratio 2) -> combine

Ideas:
- For each pair, select the max
    + max of the two ratios
    + what do we do with the city names?
      A: keep the one with the larger ratio
- explicit pseudocode:
  f((city name 1, ratio 1), (city name 2, ratio 2))
  if ratio1 > ratio2:
      return (city name 1, ratio 1)
  else:
      return (city name 2, ratio 2)

What seemed like a simple/easy idea
(calculate avg for each row, calculate max of the avgs)
gets slightly more tricky when we have to figure out exactly
what to use for the types v1 and v2,
and in particular our v2 needs not just the avg, but the city name.

Moral: figure out the data that you need, and write down
explicitly the types v1 and v2.

=== Some history ===

MapReduce was originally created by
Jeffrey Dean and Sanjay Ghemawat at Google to simplify the large-scale data processing jobs that
engineers were running on Google clusters.

One of the paper readings from Wednesday asked you to read the original paper:

    MapReduce: Simplified Data Processing on Large Clusters
    https://dl.acm.org/doi/pdf/10.1145/1327452.1327492

(BTW, this paper is very famous. Probably one of the most cited papers ever with
23,309 citations (last I checked))

Blog article: "The Friendship That Made Google Huge"

    "Coding together at the same computer, Jeff Dean and Sanjay Ghemawat changed the course of the company—and the Internet."
    https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge

=== Fully general case ===

We stated last time that MapReduce is slightly more general than the above.

Two limitations with what we did above:

L1. In the map stage, for each input row, we had to produce
    **exactly one** output row.

    This turns out to be a problem.
    Think about filter.
    If I have to produce exactly one value per input row,
    how would I do a filter?
    - Output could be 0 or 1, 0 if predicate is not true, 1 if it is true
    - Use null values, None if the predicate is not true.

    But this isn't very efficient.

    General version of MapReduce: intermediate output can
    be **list** of values.
    ---> If we want a filter, we would output empty list []
    ---> we could also output more than one item if we want.

L2. In the reduce stage, we always end up with just a single answer!
In our example, we were left with just one value (city name, global max)
What if we want to produce more than one value as output?
Maybe I want one maximum city per state, for example.

    General version of MapReduce: both stages are partitioned
    by key, Reduce stage computes one answer per key.

In the paper, Dean and Ghemawat propose the more general version of map and reduce,
which we will cover now (see Sec 2.2):

    map: (k1, v1) -> list((k2, v2))
    reduce: (k2, list(v2)) -> list(v2)

    ---> map computes 0 or more answer
    ---> reduce computes one answer per key (value of type k2)

===== Cut, skip to the bottom =====
This material was cut from the lecture,
instead, some of it will appear as exercises on HW2.

The above is written very abstractly, what does it mean?

Let's walk through each part:

Keys:

The first thing I want to point out is that all the data is given as
    (key, value)

pairs. (k1 and k2)

Generally speaking, we use the first coordinate (key) for partitioning,
and the second one to compute values.

Ignore the keys for now, we'll come back to that.

Map:
    map: (k1, v1) -> list((k2, v2))

- we might want to transform the data into a different type
    v1 and v2
- we might want to output zero or more than one output -- why?
    list(k2, v2)

Examples:
(write pseudocode for the corresponding lambda function)

- Compute a list of all Carbon-Fluorine bonds

- Compute the total number of Carbon-Fluorine bonds

- Compute the average of the ratio F / C for every molecule that has at least one Carbon
  (our original example)

In Spark:
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.flatMap.html
"""

def map_general_ex(rdd, f):
    # TODO
    raise NotImplementedError

# Uncomment to run
# map_general_ex()

"""
What about Reduce?

    reduce: (k2, list(v2)) -> list(v2)

The following is a common special case:

    reduce_by_key: (v2, v2) -> v2

Reduce:
- data has keys attached. Keys are used for partitioning
- we aggregate the values *by key* instead of over the entire dataset.

Examples:
(write the corresponding Python lambda function)
(you can use the simpler reduce_by_key version)

- To compute a total for each key?

- To compute a count for each key?

- To compute an average for each key?

- To compute an average over the entire dataset?

Important note:
k1 and k2 are different! Why?

In Spark:

https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.reduceByKey.html
"""

def reduce_general(rdd, f):
    # TODO
    raise NotImplementedError

"""
Finally, let's use our generalized map and reduce functions to re-implement our original task,
computing the average Fluorine-to-Carbon ratio in our chemical
dataset, among molecules with at least one Carbon.
"""

def fluorine_carbon_ratio_map_reduce(data):
    # TODO
    raise NotImplementedError

"""
=== Additional exercises ===
(Depending on extra time)

Some additional MapReduce exercises in exercises.py.

=== End note: Latency/throughput tradeoff ===

So, we know how to build distributed pipelines.

The **only** change from a sequential pipline is that
tasks work over scalable collection types, instead of regular data types.
Tasks are then interpreted as operators over the scalable collections.
In other words, data parallelism comes for free!

Scalable collections are a good way to think about parallel AND/OR distributed
pipelines. Operators/tasks can be:
- lazy or not lazy (how they are evaluated)
- wide or narrow (how data is partitioned)

But there is just one problem with what we have so far :)
Spark and MapReduce are optimized for throughput.
It's what we call a *batch processing engine.* That means?

A: It processes all the data, then comes back with an answer

But doesn't optimizing for throughput always optimize for latency? Not necessarily!

Let's talk a little bit about latency...

=== Understanding latency (intuitive) ===

This is related to the last question on Q10 of the midterm.

A more intuitive real-world example:
imagine a restaurant that has to process lots of orders.

- Throughput is how many orders we were able to process per hour.

- Latency is how long *one* person waits for their order.

Some of you wrote on the midterm: throughput != 1 / latency

These are not the same! Why not? Two extreme cases:

***** Finish this up on Monday. *****

Suppose the restuarant processes 10 orders over the course of being open for 1 hour

Throughput =
    10 orders / hour

Latency is not the same as 1 / throughput! Two extreme cases:

1.
    Every customer waits for the entire hour!
    Every customer submitted their order at the start of the hour,
    and got it back at the end.

    Latency = 1 hour
        (customers are not very happy)

2.
    One order submitted every 6 minutes,
    and completed 6 minutes later.

    Latency = 6 minutes
        (customers are happy)

    (A more abstract example of this is given below in the "Understanding latency (abstract)" section below.)

Throughput is the same in both cases!
10 events / 1 hour

(The first scenario is similar to a parallel execution,
the second scenario more similar to a sequential execution.)

The other formula which is not true:

    Latency != total time / number of orders
    True in the second scenario but not in the first scenario.

How can we visualize this?

    (Draw a timeline from 0 to 1 hour and draw a line for each order)

So, optimizing latency can look very different from optimizing throughput.

In a batch processing framework like Spark,
it waits until we ask, and then collects *all* results at once!
So we always get the worst possible latency, in fact we get the maximum latency
on each individual item. We don't get some results sooner and some results later.

Grouping together items (via lazy transformations) helps optimize the pipeline, but it
*doesn't* necessarily help get results as soon as possible when they're needed.
(Remember: laziness poll/example)
That's why there is a tradeoff between throughput and latency.

    "To achieve low latency, a system must be able to perform
    message processing without having a costly storage operation in
    the critical processing path...messages should be processed “in-stream” as
    they fly by."

    From "The 8 Requirements of Real-Time Stream Processing":
    Mike Stonebraker, Ugur Çetintemel, and Stan Zdonik
    https://cs.brown.edu/~ugur/8rulesSigRec.pdf

Another term for the applications that require low latency requirements (typically, sub-second, sometimes
milliseconds) is "real-time" applications or "streaming" applications.

=== Summary: disadvantages of Spark ===

So that's where we're going next,
talking about applications where you might want your pipeline to respond in real time to data that
is coming in.
We'll use a different API in Spark called Spark Structured Streaming.
"""

# **** End ****

"""
=== Cut material ===

===== Understanding latency (abstract) =====
(review if you are interested in a more abstract view)

Why isn't optimizing latency the same as optimizing for throughput?

First of all, what is latency?
Imagine this. I have 10M inputs, my pipeline processes 1M inputs/sec (pretty well parallelized.

    (input)   --- (process)
      10M        1M / sec

Latency is always about response time.
To have a latency you have to know what change or input you're making to the system,
and what result you want to observe -- the latency is the difference (in time)
between the two.

Latency is always measured in seconds; it's not a time "per item" or dividing the total time by number
of items (that doesn't tell us how long it took to see a response for each individual item!)

So, what's the latency if I just put 1 item into the pipeline?
(That is, I run on an input of just 1 item, and wait for a response to come back)?

We can't say! We don't know for example, whether the
1M inputs/sec means all 1M are processed in parallel, and they all take 1 second,
or the 1M inputs/sec means that
it's really 100K inputs every tenth of a second at a time.

This is why:
    Latency DOES NOT = 1 / throughput
in general and it's also why optimizing for throughput doesn't always benefit latency
(or vice versa).
We will get to this more in the next lecture.
"""
