"""
Part 4: Partitioning

=== Discussion Question & Poll ===

An exercise on MapReduce:

Describe how you might do the following task as a MapReduce computation.

Input dataset:
US state, city name, population, avg temperature

"Find the city with the largest temperature per unit population"

Map stage:
(For each row, output ...)

- divide the temperature by the population
- add a new column, save the new value in a new column

What are the types?
Map: for each item of type T1, output an item of type T2
T1 = (state, city name, population, avg temperature)

- T2 = (temperature / population)
- T2 = (state, city name, population, avg temp, temperature / population)

Minimal info we need:
- T2 = (city name, temp / population)

Pseudocode:
f((state, city name, population, avg temperature)):
    return (city name, temp / population)

Reduce stage:
(For each pair of results r1 and r2, combine them to get ...)

- (T2, T2) -> T2
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
what to use for the types T1 and T2,
and in particular our T2 needs not just the avg, but the city name.

Moral: figure out the data that you need, and write down
explicitly the types T1 and T2.

=== Revisiting RDDs ===

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

All operators fit into this dichotomy:
- Mapper-style operators are local, can be narrow, and can be lazy
- Reducer-style operators are global, usually wide, and not lazy.

"""

"""
=== Poll ===

Consider the following scenario where a temperature dataset is partitioned in Spark across several locations. Which of the following tasks on the input dataset could be done with a narrow operator, and which would require a wide operator?

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
