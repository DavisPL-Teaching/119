"""
Lecture 6: Streaming Pipelines

Part 1: Introduction to Streaming

=== Poll ===

Which of the following are disadvantages with MapReduce and Spark?

.
.
.

=== Outline ===

In this lecture I want to make the following take-away points:

1. Latency matters (for some applications)

2. Time is complicated

Terminology:

- Latency (revisited)

- Batch vs. Streaming

- Real-time, event time, system time, processing time

=== Latency in Spark ===

Let's start with an example to illustrate the problem with latency in Spark.

Imagine we are running something like Amazon.com. Orders are coming in through
the website to our backend data pipeline and they will be used to process orders and
update Amazon's database of how many items it has
(as well as other metadata associated with items).

Let's start with our boilerplate code as always:
"""

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("OrderProcessing").getOrCreate()
sc = spark.sparkContext

import time

"""
Here's a toy example dataset which conveys the main idea:
"""

# ***** everything comes in here *****
# start_time = time.time()
orders = [
    {"order_number": 1, "item": "Apple", "timestamp": "2024-11-24 10:00:00", "qty": 2},
    {"order_number": 2, "item": "Banana", "timestamp": "2024-11-24 10:01:00", "qty": 3},
    {"order_number": 3, "item": "Orange", "timestamp": "2024-11-24 10:02:00", "qty": 1},
    {"order_number": 4, "item": "Apple", "timestamp": "2024-11-24 10:03:00", "qty": 2},
    {"order_number": 5, "item": "Banana", "timestamp": "2024-11-24 10:04:00", "qty": 1},
    {"order_number": 6, "item": "Orange", "timestamp": "2024-11-24 10:05:00", "qty": 1},
]

"""
Let's look at the latency of an example pipeline in Spark:
"""

def process_orders_batch(orders):
    # Load orders as a Spark RDD
    # We need to simulate a smaller number of partitions
    # (we will see why later).
    orders_rdd = sc.parallelize(orders, 2)

    # (You could also do this with a DataFrame, using:
    #  orders_df = spark.createDataFrame(orders)
    #  and to set partitions to 2, orders_df.repartition(2)
    #  we'll stick to RDDs because flatMap is easier on RDDs.)

    # For each order, to simulate processing, let's sleep for a second,
    # then put one order in the output per input quantity.

    def expand_order(order):
        return [(order["order_number"], order["item"])] * order["qty"]

    def process_order(order):
        time.sleep(1) # sleep for one second
        return order

    # What flatMap does is replaces each row with a list of rows
    output = orders_rdd.flatMap(expand_order).map(process_order)

    # Ignore this for now
    output.foreach(lambda x: print(f"Processed order: {x}"))

    # Return the result
    result = output.collect()
    print("Done processing orders")
    return result

# Uncomment to run
# result = process_orders_batch(orders)
# print(result)
# ***** everything is finished here *****
# end_time = time.time()

# print(f"Latency for item X: {end_time - start_time}")

"""
How to measure latency?

On Homework 1, we limited the input dataset to just one item.
In our case, we have 6 orders, so we would limit the input dataset to just 1 order.

Then we would use the formula:
    latency = (end_time - start_time)

This was a simplified model.
Imagine the restaurant analogy again.
It's like saying, to measure how long it takes for an order,
let's just limit the number of customers allowed in the restaurant to 1,
and see how long it takes to complete their order.

Problem with this?
    - Not every order would take the same length! Some orders might take
      longer than others
    - If you're processing multiple orders at the same time, that might
      make it longer to process the orders!
      If your restaurant is busy, it might be harder to process orders on time.

What we did on HW1 is an optimistic case; it's assuming that other orders
coming in don't intefere with the one that we're measuring.

Main point: In general, just looking at an input dataset of 1 item is not sufficient.

The fully general formula is:

    latency for item X
        latency_X = (end_time_X - start_time_X)

    avg latency =
             (sum over all items X) latency_X
            ----------------------------------
                 number of items

What does latency mean for our real-world example?

    - latency_X ==> it's the time taken to process some Amazon.com user's order.
    the actual thing the user cares about.

OK, so let's apply our formula.
We have to pick an item X to measure latency for.
Let's do that below:

We can use time.time() to get the time.

Basically we have to consider where to insert:
start_time = time.time()
complete_time = time.time()

Ideas?
    start time? We could use the timestamp on the event.
    (Yes, that's one way that is used in practice!)
    Implement some sort of logger for when items come in and go out?

Conclusion:
This pipeline is not set up in such a way to measure the progress of
individual items.
I have to collect all orders, put them through the system,
and collect all outputs, before I can see the results.

The latency of any individual item X, is the same as the latency of the whole
pipeline!

This is called the "batch processing" model.
MapReduce and Spark are both batch processors.

Orders are grouped into "batches" and processed all as one group.
"""

# Uncomment
# result = process_orders_batch(orders)
# print(result)
# latency = TODO
# print(f"Latency: {latency} seconds")

"""
How can we do better?

(Think about it in terms of the real-world scenario)

    Basically it was like the scenario 1 in the endnote
    to lecture 5.

    We want to do more like scenario 2, instead.

Main idea to fix it:
Try uncommenting the "output.foreach" line above that we ignored.
This is basicaly the first step to fixing our pipeline.

We get to see the results come out as items are processed!

That's what we're trying to do going forward, and the Spark Streaming
API will make this easier.





Recap on latency:
- Latency = Response Time
- Latency can only be measured by focusing on a single item or row. (response time on that row)
- Latency-critical, real-time, or streaming applications are those for which we are looking for low latency (typically, sub-second or even millisecond response times).
- Latency is not the same as 1 / Throughput
    + If it were, we wouldn't need two different words!
- Latency is not the same as processing time
    + It's processing time for a specific event
- If throughput is about quantity (how many orders processed), latency is about quality (how fast individual orders processed).

In contrast to "batch processing", "streaming" applications process each item as soon as it arrives.
It is a good model for optimizing latency of a pipeline.
"""
