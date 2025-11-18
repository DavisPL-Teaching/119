"""
Lecture 5, Part 2:
Properties of RDDs

=== Properties of scalable collection types ===

We will see that

    RDDs are: scalable, (data-)parallel, lazy, immutable, partitioned, and fault-tolerant.

    (Recall: scalable collection types = data parallelism)

    Operators on RDDs create dataflow graphs! (more on this soon)

We have seen the first 2 properties.
We will cover the 3rd and 4th and get to the 5th one in Part 4.

Not just about RDDs!

---> Most of this generalizes to all distributed programming contexts.

=== Discussion Question & Poll ===

https://forms.gle/XqVuiQw8WFRUBku69

Which of the following can NOT easily be converted into an operator over a scalable collection type?
(Select all that apply)

1. From each country in a dataset, extract the capital city column

2. Match each employee in a name_table with their salary in salary_table

3. Add up all the integers between 1 and 100,000,000

4. Given a dataset containing (t, x, y, z) points in a single airplane's flight path,
   where t is the time and (x, y, z) is the 3D location of the plane, determine
   the total **time** traveled by the plane

5. Given a dataset containing (t, x, y, z) points in a single airplane's flight path,
    where t is the time and (x, y, z) is the 3D location of the plane, determine
    the total **distance** traveled by the plane

6. Given a dataset containing (t, x, y, z) points in a single airplane's flight path,
   where t is the time and (x, y, z) is the 3D location of the plane, fill in any
   missing points along the flight path where "missing point" is determined by
   interpolating between the adjacent flight path points.

(For fun, optional:)

7. Given a dataset containing (t, x, y, z) points in a single airplane's flight path,
   where t is the time and (x, y, z) is the 3D location of the plane, determine
   the **average velocity** traveled by the plane

8. Given a dataset containing (t, x, y, z) points in a single airplane's flight path,
   where t is the time and (x, y, z) is the 3D location of the plane, determine
   the **average speed** traveled by the plane

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

Answers:
5, 6, and 8

Takeaway: These are just about data parallelism
Think about splitting the dataset in half
5, 6: if split in half, two adjacent points in the path might end up in different halves
8: similar reason, 7 can be done technically as avg velocity = (final point - begin point) / (total time).

=== Laziness ===

What is laziness?

    Definition: A operator (or computer program)
    is **lazy** if it delays computing answers until
    you ask for them, as much as possible.

    Spark is lazy and does the above.
    (Dask does the same thing -- we saw a very brief example)

First, a running example.

A toy chemical dataset:
"""

# Boilerplate from part 1
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
sc = spark.sparkContext

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
    # breakpoint()

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
    # BTW: can add ! at the start of a command in PDB to run a regular Python command

    # Uncomment to run and inspect
    # return rdd1, rdd2, rdd3

# Uncomment to run
# fluorine_carbon_ratio(CHEM_DATA)

# Uncomment to run with -i
# rdd1, rdd2, rdd3 = fluorine_carbon_ratio(CHEM_DATA)

"""
In Spark, and in particular on RDDs,
operators are divided into *transformations* and *actions.*

https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html

Transformation: transform the data without computing the answer (yet)
Action: compute an answer

In other words...

Terminology (this comes from programming language design):
    (e.g. Haskell is lazy)
Transformations are also called "lazy" operators
and actions are not lazy (also called "eager" operators)

How can we determine which of the above are transformations and which are actions?

Ideas?

- Print it out!

  Transformation = prints out as an RDD (it's just a blob that doesn't have any data output)

    After a transformation: PythonRDD[3] at RDD at PythonRDD.scala:53

  Action = prints out as Python data.

    After an action: (count: 3, mean: 0.625, stdev: 0.8838834764831844, max: 1.875, min: 0.0)

Answers:

Transformations (lazy):
    Will always return RDDs

- .map(), .filter()

Actions (not lazy):
    Will directly return Python results

- .stats()
"""

"""

Why Laziness?

You might wonder: why not just compute all the answers up front?

Conjectures?

- If you're pipelining the output, you could save memory!
  (operator1) --> (operator2)
  Doing operator1, then operator2 is ineficient (lots of stuff stored in memory)
  (and we didn't anything in parallel)
  Doing them both at once allows Spark to optimize the pair of them together.

- More generally: we want to optimize the pipeline before running it.
"""

"""
=== More examples of laziness ===

More examples of transformations are:

- .map
- .filter
- .sample(withReplacement, fraction)
- .distinct()

Some examples of actions are:

- .collect()
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
Dataflow graph:

                                    -> (stats)
(load inpput) -> (filter) -> (map)
                                    -> (mean)

                 ^^^^^^^^^^^transformations
                                        ^^^^^^^^^ actions

=== Visualizing the dataflow graph ===

All distributed pipelines can be viewed as dataflow graphs.

What is the connection between RDDs and dataflow graphs?

Q: let's draw the above as a dataflow graph using ASCII art.

(What are our tasks/nodes and arrows?)

    Tasks: Operators that were done on the RDD
    Arrows: dependencies from one operator to another

    Our dataflow graph:

    *** FILL OUT ***

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

Can we view this more programmatically?

Unfortunately the visualization capabilities of RDDs are a bit limited.
Two ways for now:
Both of these are not super helpful and don't give precise information.

- Go to localhost:4040/
- .toDebugString()

There is a better way available when we get to DataFrames.
"""

# Try going to localhost:4040/

# Try .toDebugString()

"""
We saw: Laziness in RDDs

We worked through a chemistry dataset example -- transformations and actions

We will pick this up on Monday.

***** Where we ended for today *****

=== Additional properties: ===

===== Immutability =====

Let's illustrate this:

Exercise: try this:
- Create an RDD
- Get one or more of the rows
- Modify the result

Useful commands:
    - .collect()
    - .first()
    - .take(n) # first n rows

What happened?

It didn't work - even after modifying the list after
    l = rdd.first()
we were unable to see those changes in the original RDD.

RDDs are immutable: you can't modify them!

===== Fault tolerance =====

Recall: def. of distribution, why faults are a particular concern

    PySpark jobs or RDD operations can be distributed and run in parallel
    over multiple!

    Multiple warehouses running separate computations

    Part of the problem of running distributed code is that one
    warehouse (machine) can fail, while another warehouse (machine) is
    still running.

    We want to silently recover in case of errors.

    This is a property known as "fault tolerance"

    Your pipeline is tolerant to faults, network failures, or crashes

RDD data will try to automatically recover if a node (worker or machine) crashes
It does this while still mostly maintaining data in-memory, which is impressive.

We will not have time to cover this in detail in this lecture!

I can do an extra lecture on distributed consistency and distributed algorithms if there is interest.

We will just assume PySpark gives us correct results.

=== Wrapping up ===

We saw Laziness of RDDs: all RDD operators are divided into lazy transformations
(which return another RDD object/handle and don't compute anything)
and non-lazy actions (which return result data in plain Python)

We saw that all computations over RDDs are really dataflow graphs.
    code == dataflow graph

RDDs are: scalable, (data-)parallel, lazy, immutable, partitioned, and fault-tolerant.
                                                      ^^^part 4
"""
