"""
Part 5: DataFrames

(We will skip over most of this part due to time)

=== Discussion Question & Poll ===

This was the poll I accidentally shared last time :-)

https://forms.gle/TB823v4HSWqYadP88

Consider the following scenario where a temperature dataset is partitioned in Spark across several locations. Which of the following tasks on the input dataset can be done with a narrow operator, and which will require a wide operator?

Assume the input dataset consists of locations:
US state, city, population, avg temperature

It is partitioned into one dataset per US state (50 partitions total).

1. Add one to each temperature

2. Compute a 5-number summary

3. Throw out duplicate city names (multiple cities in the US with the same name)

4. Throw out cities that are below 100,000 residents

5. Throw out "outlier" temperatures below -50 F or above 150 F

6. Throw out "outlier" temperatures 3 std deviations above or 3 std deviations below the mean

7. Filter the dataset to include only California cities

.
.
.
.
.

==================

We said that PySpark supports at least two scalable collection types.

Our first example was RDDs.

Our second example of a collection type is DataFrame.
"""

# Boilerplate and dataset from previous part
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkExample").getOrCreate()
sc = spark.sparkContext

CHEM_NAMES = [None, "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"]
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
    df5 = df4.withColumn("H + F", col("H") + col("F"))

    # This is the equiv of Pandas: df3["H + C"] = df3["H"] + df3["C"]

    # Uncomment to debug:
    # breakpoint()

    # We could continue this example further (showing other Pandas operation equivalents).

# Uncomment to run
# ex_dataframe(CHEM_DATA)

"""
use .show()! - nicer version of .collect()!
Only available on dataframes.

=== Web interface ===

Revisiting the web interface & dataflow graph

localhost:4040/

(see under Stages and click on a "collect" job for the dataflow graph)

=== Extras ===

Another misc. DataFrame example can be found in
extras/dataframe.py.

(feel free to uncomment and play with it offline)

=== Advantages of DataFrames? ===

Higher level than RDDs, more structured.

We can work directly with SQL and relational abstractions.
"""
