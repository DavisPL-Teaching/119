"""
Part 4: Partitioning

=== Discussion Question & Poll ===

An exercise on MapReduce:

Describe how you might do the following task as a MapReduce computation.

Input dataset:
US state, city name, population, avg temperature

"Find the city with the largest temperature per unit population"

https://forms.gle/VpXZ3c9Zam7SxFVi7

Answer (go through together):

Map stage:

    What to do:
    For each input row, map that input row to ....

    f: T1 -> T2

Reduce:

    Describe what to do for a pair of output rows

    f: T2 x T2 -> T2

What are the types?
Map: for each item of type T1, output an item of type T2

- T1

- T2

After the map stage, what info do we need?

    - don't need the state

    - DO need the city

    - Do need the ratio: (avg temperature) / population

Idea for map stage (in words):

    For each row, return the ordered pair

        (city, (avg temp) / (population))

Reduce stage:

Take a pair of output rows, and return one output row.

    Find the max of the two output rows! Since we are
    trying to find the maximum average temperature.

    Reduce stage input? Two rows:

        (city1, (avg temp1) / (population1))

        (city2, (avg temp2) / (population2))

    Or if you like:

        (city1, ratio1)

        (city2, ratio2)

    We must return something of the form:

        (city3, ratio3)

    We know that ratio3 should be max(ratio1, ratio2)

    We see which of ratio1 and ratio2 is bigger

    What should do for city3?
    --> We should pick whichever city was accompanied by
        the bigger ratio

    Pseudocode:

        if ratio1 < ratio2:

            return (city2, ratio2)

        else:

            return (city1, ratio1)

What was T1 and what was T2?

    input: US state, city name, population, avg temperature
    T1 = (string, string, integer, float)

    T2 = (string, float)

The tricky thing is that reduce must be of the form

    T2 x T2 -> T2

=== Comment ===

What seemed like a simple/easy idea
(calculate avg for each row, calculate max of the avgs)
gets slightly more tricky when we have to figure out exactly
what to use for the types T1 and T2,
and in particular our T2 needs not just the avg, but the city name.

Moral: figure out the data that you need, and write down
explicitly the types T1 and T2.

You can't go back to the original dataset in your map stage!
Your map stage must therefore return all information you
need as part of the type T2.

--------------------------------------

=== Revisiting RDDs ===

MapReduce has taught us that for general distributed data processing, we only need two things:

1. a way of transforming values "locally" (at each distributed node or parallel worker - no coordination!)

2. a way of combining results (from different distributed nodes or parallel workers) to get a final answer

But even the combining results part is done "per key" in general! This helps immensely
as it means that even this stage can be done in a data-parallel way.

This brings us to our last property of RDDs (an important one!): Partitioning!
"""

# Boilerplate and dataset from previous part
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
sc = spark.sparkContext

CHEM_DATA = {
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

"""
=== Partitioning ===

Whenever we consruct an RDD, under the hood it is going to be partitioned
into several chunks or subsets of the data; these could be all stored on the same machine,
or they could be stored on separate distributed machines.

Partitioning is what makes RDDs a scalable collection type.
It's how Spark implements data parallelism.

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
- 8
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

# Exercise: using the number of partitions as an optional parameter, print:
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

Try it out:
Run
    show_partitions(CHEM_DATA, 1000)

    show_partitions(CHEM_DATA, 10000)

What happens?

Moral of the story:
In an ideal world, we wouldn't worry about partitioning,
however, in practice, we may need to configure the number of partitions
in Spark for various reasons (availability of compute, how many nodes we
want to allocate, etc.)

If the number of partitions created is wildly off from the
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

Recap:

- we did a practice MapReduce question on the poll

    + think about what intermediate output you need to store in order to
      compute a query

    + think about what the types T1 and T2 need to be
      (without keys, reduce must always be a function taking two items of type T2
       and returning a single item of type T2)

- we saw that RDDs implement data parallelism via partitioning

    + we saw that one can set and view the number of partitions

    + generally in an ideal world, we would not worry about the # of partitions

      however, having too few or too many partitions can severely impact
      pipeline performance.

------------------

(picking up here on Friday, Nov 21)

One note from after class last time!

Partitioning = Sharding.
It's the same concept.

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

A:

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

"""

"""
=== Example operators ===

All operators fit into this dichotomy:
- Mapper-style operators are local, narrow, and usually lazy
- Reducer-style operators are global, usually wide, and usually not lazy.

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
=== Other miscellaneous partitioning-related operations ===
(Skip for time)

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
