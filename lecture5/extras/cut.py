
"""
=== Cut material ===

===== Cut material on MapReduce =====

Some of this material will appear as exercises on HW2.

The above is written very abstractly, what does it mean?

Let's walk through each part:

Keys:

The first thing I want to point out is that all the data is given as
    (key, value)

pairs. (K1 and K2)

Generally speaking, we use the first coordinate (key) for partitioning,
and the second one to compute values.

Ignore the keys for now, we'll come back to that.

Map:
    map: (K1, T1) -> list((K2, T2))

- we might want to transform the data into a different type
    T1 and T2
- we might want to output zero or more than one output -- why?
    list(K2, T2)

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

    reduce: (K2, list(T2)) -> list(T2)

The following is a common special case:

    reduce_by_key: (T2, T2) -> T2

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
K1 and K2 are different! Why?

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
We will get to this more in Lecture 6.
"""
