"""
Lecture 5, Part 2:
Properties of RDDs
and
Laziness

=== Properties of scalable collection types ===

We will see that
    RDDs are: scalable, parallel, lazy, immutable, partitioned, and fault-tolerant.

    Operators on RDDs create dataflow graphs! (more on this soon)

We have seen the first 2 properties.
We will cover the 3rd and 4th and get to the 5th one in Part 4.

Not just about RDDs!

---> Most of this generalizes to all distributed programming contexts.

=== Poll ===

Review question about RDDs:



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

=== Visualizing the dataflow graph ===

All distributed pipelines can be viewed as dataflow graphs.

What is the connection between RDDs and dataflow graphs?

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
=== Additional properties ===

- Immutability

Let's illustrate this:

Exercise: try this:
- Create an RDD
- Collect
- Modify the result
What happens?

(It doesn't work)

- Fault tolerance

RDD data will actually automatically recover if a node (worker or machine) crashes
It does this while still mostly maintaining data in-memory, which is impressive.

=== Wrapping up ===

We saw Laziness of RDDs: all RDD operators are divided into transformations
(which return another RDD object/handle and don't compute anything)
and actions (which return result data in plain Python)

We saw that all computations over RDDs are really dataflow graphs.
    code == dataflow graph
"""
