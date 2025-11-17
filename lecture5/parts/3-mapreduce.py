"""
Part 3: MapReduce

=== Discussion Question & Poll ===

An exercise on laziness:

https://forms.gle/zFjVES96i5jjnMCRA

Suppose we want to do 3 tasks:

1. Generate 100,000 random data points (vectors v)
2. Map each data point v to a normalized vector v / ||v||
3. Print the first 5 answers

As a dataflow graph:
(1) ---> (2) ---> (3)

We want to know which of 1, 2, 3 should be lazy, and which should be evaluated right away.

Which tasks should be executed lazily if we want to get the answer in the most efficient way?

Bonus:
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
you can create, with just two stages!
It's a dataflow graph with just three nodes:

    (input) ---> (map) ---> (reduce).

The kind of amazing thing is that essentially all operators on distributed
pipelines can be reduced down to this simple form,
called a MapReduce job.
(Sometimes you might you need more than one MapReduce job to get some computations
done.)

=== Definitions ===

Map stage:
    - Take our input a scalable collection of items of type T, and apply
      the same function f: T1 -> T2 to all inputs.

      (T, U could be, integers, floats, chemicals, rows, anything)

Reduce stage:
(This differs a little by implementation)
    - a way of combining two different intermediate outputs:
      a function f: T2 x T2 -> T2.

=== Examples ===

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

We have actually been writing MapReduce pipelines all along!
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
    rdd: RDD where the items have type T1
    f: a function T1 -> T2
    output: RDD where the items have type T2

    Apply the f to each input item
    """
    rdd2 = rdd.map(f)

    # Uncomment to show intermediate stage
    print(f"Intermediate: {rdd2.collect()}")

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
    res1 = map(rdd, lambda x: x[1])

    # reduce should just add together integers
    # T2 = integer
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
=== Some history ===

MapReduce was originally created by
Jeffrey Dean and Sanjay Ghemawat at Google to simplify the large-scale data processing jobs that
engineers were running on Google clusters.

Here is the original paper:

    MapReduce: Simplified Data Processing on Large Clusters
    https://dl.acm.org/doi/pdf/10.1145/1327452.1327492

(BTW, this paper is very famous. Probably one of the most cited papers ever with
almost 25,000 citations (last I checked))

Blog article: "The Friendship That Made Google Huge"

    "Coding together at the same computer, Jeff Dean and Sanjay Ghemawat changed the course of the company—and the Internet."
    https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge

=== Fully general case ===

This is only very slightly simplified. Two things to make it general:

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
    ---> reduce computes one answer per key (value of type K2)
"""

"""
=== MapReduce and DataFrames ===

(We may skip some of this for time)

DataFrames are based on RDDs and RDDs are based on MapReduce!
A little picture:

  DataFrames
  |
  RDDs
  |
  MapReduce

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

=== Additional exercises ===
(Depending on extra time)

Some additional MapReduce exercises in extras/exercises.py.

Cut material that will appear as part of HW2 in extras/cut.py
"""
