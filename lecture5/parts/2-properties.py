"""
Lecture 5, Part 2:
Properties of RDDs

=== Poll ===

Speedup through parallelism alone (vertical scaling) is significantly limited by...
(Select all that apply)

1. The number of lines in the Python source code
2. The version of the operating system (e.g., MacOS Sonoma)
3. The number of CPU cores on the machine
4. The number of wire connections on the computer's motherboard
5. The amount of RAM (memory) and disk space (storage) available

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
"""
