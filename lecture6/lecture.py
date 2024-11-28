"""
Lecture 6: Streaming Pipelines

=== Poll ===

Which of the following are disadvantages with MapReduce and Spark?

https://forms.gle/83czz2QBH1mu5cse8

=== Outline ===

Today's lecture I want to make the following take-away points:

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

***** where we stopped for Nov 25 *****

=================================================

=== Nov 27 ===

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

=== Poll ===

Which of the following are most likely application scenarios for which latency matters?

https://forms.gle/Yaqe69zwBwYD91Fz8

Latency doesn't always matter, but for some applications, it matters a lot.

=== Spark Streaming ===

In particular: Structured Streaming
Structured = using relational and SQL abstractions
Structured Streaming syntax is similar (often almost identical) to Spark DataFrames

There's an analogy going on here!
Batch processing application using DataFrames <---> Streaming application using Structured Streaming

Let's see an actually streaming example.
"""

# New imports
from pyspark.sql.functions import array_repeat, from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define the schema of the incoming JSON data
schema = StructType([
    StructField("order_number", IntegerType()),
    StructField("item", StringType()),
    StructField("timestamp", StringType()),
    StructField("qty", IntegerType())
])

def process_orders_stream(order_stream):
    """
    important:
    order_stream: now a stream handle, instead of a list of plain data!
    """

    # Parse the JSON data
    df0 = order_stream.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))

    # First cut: just return the parsed orders
    # return df0

    ### Full computation

    # df0 is all bunched up in a single column, can we expand it?

    # Yes: select the data we want
    df1 = df0.select(
        col("parsed_value.order_number").alias("order_number"),
        col("parsed_value.item").alias("item"),
        col("parsed_value.timestamp").alias("timestamp"),
        col("parsed_value.qty").alias("qty")
    )

    # (Notice this looks very similar to SQL!
    # Structured Streams uses an almost identical API to Spark DataFrames.)

    # return df1

    # Create a new field which is a list [item, item, ...] for each qty
    df2 = df1.withColumn("order_numbers", array_repeat(col("order_number"), col("qty")))

    # Explode the list into separate rows
    df3 = df2.select(explode(col("order_numbers")).alias("order_number"), col("item"), col("timestamp"))

    return df3

"""
We need to decide where to get our input! Spark supports getting input from:
- Apache Kafka (good production option)
- Files on a distributed file system (HDFS, S3)
- A network socket (basically a connection to some other worker process or network service)

We're looking for a toy example, so let's use a plain socket.

This will require us to open up another terminal and run the following command:

        nc -lk 9999

"""
# (Uncomment to run)
# Set up the input stream using a local network socket
order_stream = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Call the function
out_stream = process_orders_stream(order_stream)

# Print the output stream and run the computation
out = out_stream.writeStream.outputMode("append").format("console").start()
out.awaitTermination()

"""
There are actually two streaming APIs in Spark,
the old DStream API and the newer Structured Streaming API.

Above uses the Structured Streaming API (which is more modern and flexible
and solves some problems with DStreams, I also personally found it better
to work with on my machine.)

=== Q + A ===

Q: How is the syntax different from a batch pipeline?

A: It's nearly identical to DataFrames, except the input/output
    input: pass in a stream instead of a dataframe
    output: we call .writeStream.outputMode(...)

Q: How is the behavior different from a batch pipeline?

A:
It groups events into "microbatches", and processes each microbatch
in real time (aiming to achieve low latency)

You can also set the microbatch duration
(1 batch every 1 second, 1 batch every 0.5 seconds, 1 batch every 0.25 seconds, ...)
depending on your application needs

Q: How does Spark determine when to "run" the pipeline?

A: Calling .start()

Q: How do we know when the pipeline is finished?

A:
With .awaitTermination() we just wait for the user to terminate the connection
(ctrl-C)
You can also configure different options, for example terminate after inactivity
for 1 hour, etc.

Upshot:
input/output configuration is different,
actual application logic of the pipline is the same.

=== Microbatching ===

One thing we noted above and can see in the output is how Spark groups
items into mini DataFrame updates, called "microbatches".

(Side note: this isn't how all streaming frameworks work, but this is
the main idea behind how Spark Streaming works.)

That leads to an interesting question: how do we determine the microbatches?

Possible ways?

1. Wait 0.5 seconds, collect all items during that second and group it into a batch
2. Set a limit on the number of items per batch (e.g. 100), once you get 100
   items, close the batch
3. Set a limit on the number of items, OR wait for a 2 second timeout

It comes down to a question of "time" and how to measure progress.

Suggestion #1 measures time in terms of the operating system clock

Suggestions #2 measures time in terms of how many items arrive in the pipeline,
and uses that to decide when to move forward.

Both of these suggestions become more interesting/complicated when you consider
a distributed application, where you might have (say) 5-10 different machines
taking in input requests, and all of them have their own notion of time that
they are measuring and enforcing.

This turns out to be very important, so it is the next thing we will
cover in the context of streaming pipelines.

It is also important to how we measure latency and can be important
to the actual behavior of our pipeline.

That's a bit about why time is important, and we'll get into
different notions of time in this context next time.

***** Ended here for Nov 27 *****

====================================================

=== Time is Complicated ===

Final thing: in talking about latency, we constantly referred to time.
What is time, anyway?

Time is complicated!
Some optional but highly recommended reading:
https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca

I'd like you to know the following definitions of time:

- Real time
- Event time
- System time

Q: In the context of a streaming application, which of the above is useful?

A:

System time variants:
- OS time
- Spark time
- Arrival time
- Processing time
- Exit time

The following are also useful concepts (but not required to know for this class):
- Logical time
- Monotonic time
"""

"""
=== Exercises ===

Let's edit our streaming pipeline to log each notion of time.

Syntax we need to know:
    df.withColumn(...)

    current_timestamp()

    time.time()

New concepts:
    UDF = User Defined Function

"""

from pyspark.sql.functions import current_timestamp, udf, date_format

### Time logging UDF

from datetime import datetime

def current_system_time():
    # Return the current system time
    # Raw timestamp:
    # return time.time()
    # Pretty print the output:
    readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return readable_time

time_udf = udf(current_system_time, StringType())

def log_time(stream):
    return (
        stream
        .withColumn("system_time", time_udf())
        .withColumn("spark_timestamp", date_format(current_timestamp(), "yyyy-MM-dd HH:mm:ss"))
    )

### Delay UDF to make the computation take longer
### (Ignore this for now)

# def process_delay():
#     # Simualte a difficult processing step by inserting a delay
#     time.sleep(1)
#     return "delay applied"

# process_delay_udf = udf(process_delay, StringType())

# def log_delay(stream):
#     return stream.withColumn("delay", process_delay_udf())

def process_orders_stream(order_stream):
    # Code from before
    df0 = order_stream.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))
    df1 = df0.select(
        col("parsed_value.order_number").alias("order_number"),
        col("parsed_value.item").alias("item"),
        col("parsed_value.timestamp").alias("timestamp"),
        col("parsed_value.qty").alias("qty")
    )

    # Uncomment to include
    # df1 = log_time(df1)

    df2 = df1.withColumn("order_numbers", array_repeat(col("order_number"), col("qty")))
    df3 = df2.select(explode(col("order_numbers")).alias("order_number"), col("item"), col("timestamp"))

    # Uncomment to include
    # df3 = df2.select(explode(col("order_numbers")).alias("order_number"), col("item"), col("timestamp"), col("system_time").alias("system_time_orig"), col("spark_timestamp").alias("spark_timestamp_orig"))

    # Uncomment to include
    # df3 = log_delay(df3)

    # Uncomment to include
    # df3 = log_time(df3)

    # Return
    return df3

# (Uncomment to run)
# order_stream = spark.readStream.format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()
# out_stream = process_orders_stream(order_stream)
# out = out_stream.writeStream.outputMode("append").format("console").start()
# out.awaitTermination()

"""
Tasks:

1. Uncomment the lines to include the time logging functions.

2. Uncomment the lines to include the delay function.

3. Rename the time-related columns to make it clear which time they are:
system time, event time, arrival, processing, exit

=== Measuring latency ===

Which type of time should we use to measure latency?

Recall formula for latency:
-

Options?
-

=== Failure Cases ===

Streaming pipelines have additional failure cases from their batch counterparts.
Let's cover a few of these:

- Out-of-order data (late arrivals)

- Clock drift and non-monotonic clocks

- Too much data

.
.
.

Q: How do we deal with out-of-order data?

Q: How do we deal with clocks being wrong?

Q: How do we deal with too much data?

Q: What happens when our pipeline is overloaded with too much data, and the above techniques fail?
"""
