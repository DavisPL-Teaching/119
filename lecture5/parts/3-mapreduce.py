"""
Part 3: MapReduce

(NOTE: starting with Part 3 today, finishing Part 2 after.)

We have talked about how to view **data sets** for the purposes of distributed pipelines:
what we need is the idea of a Scalable Collection Type.

What we need now is a way to view **operators** for the purposes of distributed pipelines.
What is the distributed equivalent of an operator?

=== MapReduce ===

MapReduce is a simplified way to implement and think about
distributed pipelines.

In MapReduce there are only two operators,
Map and Reduce.

PySpark equivalents:
- .map
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.map.html
- .reduce
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.reduce.html#pyspark.RDD.reduce

Also equivalent to reduce (but needs an initial value)
- .fold
https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.fold.html

In fact, a MapReduce pipeline is the simplest possible pipeline
you can create, with just three tasks:
It's a dataflow graph with just three nodes:

    (input) ---> (map) ---> (reduce).

=== Some history ===

MapReduce was originally created by
Jeffrey Dean and Sanjay Ghemawat at Google to simplify the large-scale data processing jobs that
engineers were running on Google clusters.

Here is the original paper:

    MapReduce: Simplified Data Processing on Large Clusters
    https://dl.acm.org/doi/pdf/10.1145/1327452.1327492

(BTW, this paper is very famous. Probably one of the most cited papers ever with
over 25,000 citations on Google Scholar.)

Blog article: "The Friendship That Made Google Huge"

    "Coding together at the same computer, Jeff Dean and Sanjay Ghemawat changed the course of the
    company—and the Internet."
    https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge

The kind of amazing thing is that essentially all operators on distributed
pipelines can be reduced down to this simple form,
called a MapReduce job.
    (Insight of original MapReduce paper coming out of Google)

(Sometimes you might you need more than one MapReduce job to get some computations done.)

=== Definitions ===

Map stage:
    - Take our input a scalable collection of items of type T1, and apply
      the same function f: T1 -> T2 to all inputs.

      (T, U could be, integers, floats, chemicals, rows, anything)

      (The transformation applies to individual input rows! Data-parallel)

Reduce stage:
(This differs a little by implementation)
    - a way of combining two different intermediate outputs:
      a function f: T2 x T2 -> T2.

=== Examples ===

My input dataset consists of populations by city.
I want the total population over all cities.

If I wanted to do this as MapReduce:

Map: do nothing, on each input row x, return the population of row x
    as an integer:

        lambda x: x["population"]

Reduce: if I have two outputs x and y, return x + y

        lambda x, y: x + y.

The MapReduce computation will repeatedly apply the reduce function
until there is no more reducing to do.

    In this case:

        T1 = Rows with a population field

        T2 = Integers

        map: Row -> Integer
        reduce: Integer x Integer -> Integer

Our previous example from Part 2 is also a MapReduce function!

In our CHEM_DATA example:
- map stage: we apply a local computation to each input row: in our case,
  we wanted to get the number of fluorines / num carbons for all rows which
  have at least one carbon.
- reduce stage: we aggregate all outputs across input rows: in our case,
  we wanted to compute the avg across all inputs.

=== MapReduce in PySpark ===

Let's copy in our boilerplate from Part 1:
"""

# Boilerplate from part 1
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
sc = spark.sparkContext

"""
Chemistry dataset again, with a few more entries:
"""

# Re-defining from Part 2
# (and adding a couple more molecules)
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
    # Add your own chemicals here ...
}

# TASK:
# Compute the total number of hydrogens across all chemicals in our dataset.

# First: defining our map and reduce functions:

def map(rdd, f):
    """
    rdd: RDD where the items have type T1
    f: a function T1 -> T2
    output: RDD where the items have type T2

    Apply the f to each input item
    """
    rdd2 = rdd.map(f)

    # Uncomment to show intermediate stage
    # print(f"Intermediate: {rdd2.collect()}")

    return rdd2

def reduce(rdd, f):
    """
    rdd: RDD where the items have type T2
    f: T2 x T2 -> T2
       (T2, T2) -> T2
    output: a single value T2

    Apply the f to pairs of values until there's only one left.
    """

    return rdd.reduce(f)

# If done correctly, the following should work

def get_total_hydrogens(data):
    rdd = sc.parallelize(data.values())

    # list x, x[1] gives us the Hydrogen coordinate
    # T1 = list[integers]
    # T2 = integer
    # f: list[integers] -> integer
    # x[1] is the no. of hydrogens
    res1 = map(rdd, lambda x: x[1])

    # reduce should just add together integers
    # T2 = integer
    # f: (integer, integer) -> integer
    # Two total #s of hydrogens: take them out, add them up, put them back
    res2 = reduce(res1, lambda x, y: x + y)

    # def add(x, y):
    #     return x + y

    print(f"Result: {res2}")

    return res1, res2

# Uncomment to run
# get_total_hydrogens(CHEM_DATA)

# (Count by hand to check)
# 16 :checkmark:

# Intermediate result:  [2, 0, 0, 0, 0, 4, 6, 1, 3, 0]

# Note:
# We could also .collect() and then .parallelize() the results after the
# map stage if we wanted to simulate completing the results of the Map stage
# and reshuffling prior to getting to the Reduce stage.
# Many MapReduce implementations work this way.

"""
That's MapReduce (simple version)

There is a practice question on MapReduce, that we will do
at the start of class next time.

=== Fully general case ===

This is slightly simplified. Two things to make it general:

(You will do the general case as part of HW2!)

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

    Instead of

        f: T1 -> T2

    Map stage will use a function f of the form

        f: T1 -> List<T2>

L2. In the reduce stage, we always end up with just a single answer!
In our example, we were left with just one value (city name, global max)
What if we want to produce more than one value as output?
Maybe I want one maximum city per state, for example.

    General version of MapReduce: both stages are partitioned
    by key, Reduce stage computes one answer per key.

In the paper, Dean and Ghemawat propose the more general version of map and reduce
(See Sec 2.2),
which is covered on the homework:

    map: (K1, T1) -> list((K2, T2))
    reduce: (K2, list(T2)) -> list(T2)

    ---> map computes 0 or more answer
    ---> reduce computes 0 or more answers per key (value of type K2)

---------

=== Returning to Part 2 ===

At this point, we will return and complete the rest of Part 2.

************

************

************

====== ************ After finishing Part 2 ************ =======

************

    ***  We will return to this part and the following poll after finishing Part 2. ***

************

Note!

map is the quintessential lazy operator (transformation)

reduce is the quintessential not-lazy operator (action)

In general, most "row-level" operations are transformation, and most
aggregations are actions

=== Discussion Question & Poll ===

An exercise on laziness:

https://forms.gle/tSPBZHSCWnLoyFDb7

Suppose we want to do 3 tasks:

1. Generate 100,000 random data points (vectors v)
2. Map each data point v to a normalized vector v / ||v||
3. Print the first 5 answers

As a dataflow graph:
(1) ---> (2) ---> (3)

We want to know which of 1, 2, 3 should be lazy, and which should be evaluated right away.

Which tasks should be executed lazily if we want to get the answer in the most efficient way?

Bonus question:
If we assume that all operators take 1 ms per input that they process, how long would the pipeline take in the optimal case?

Assume that creating the dataflow graph itself doesn't take any time, only evaluating it takes time.

Assume there is no parallelism.

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

SPOILER

Workthrough: see `extra/laziness_poll_workthrough.txt`

=== Recap ===

- Motivation for MapReduce:

    + argued can express all/general distributed computations

    + Only 2 operators

- We introduced the simple form of MapReduce:

    map: f: T1 -> T2

    reduce: T2 x T2 -> T2

- We talked about limitations of the simple model, and how to generalize this:

    1. Allow zero or more outputs

    2. Attach keys to everything (K1, T1), (K2, T2)

    You will do this on your HW

- We finished talking about laziness

    Transformations = lazy, produce output an RDD

    Actions = not lazy, produce output a result

    map = quintessential example of a transformation

    reduce = quintessential example of an action

- We got some practice with laziness on the poll, that we will go over next time.

=== Additional exercises ===
(SKIP)

Some additional MapReduce exercises in extras/exercises.py.

Cut material that will appear as part of HW2 in extras/cut.py.
"""
