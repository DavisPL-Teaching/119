"""
Part 4: DataFrames

We said that PySpark supports at least two scalable collection types.

Our first example was RDDs.

Our second example of a collection type is DataFrame.

=== Discussion Question & Poll ===

An exercise on MapReduce:

Describe how you might do the following task as a MapReduce computation.

Input dataset:
US state, city name, population, avg temperature

"Find the city with the largest temperature per unit population"

https://forms.gle/YS787c6aeDe3mZR59

Answer (go through together):

Map stage:
(For each row, output ...)

- divide the temperature by the population
- add a new column, save the new value in a new column

What are the types?
Map: for each item of type T1, output an item of type T2

- T1
- T2

Minimal info we need?

Pseudocode:

Map stage:
    f(x):




Reduce stage:
    f(x, y):



.
.
.
.
.

=== Comment ===

What seemed like a simple/easy idea
(calculate avg for each row, calculate max of the avgs)
gets slightly more tricky when we have to figure out exactly
what to use for the types T1 and T2,
and in particular our T2 needs not just the avg, but the city name.

Moral: figure out the data that you need, and write down
explicitly the types T1 and T2.

=== DataFrames ===

DataFrames are based on RDDs and RDDs are based on MapReduce!
A little picture:

  DataFrames
  |
  RDDs
  |
  MapReduce

DataFrame is like a Pandas DataFrame.

https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html

An example of a dataframe computation is shown in

    cut/examples.py

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
"""
