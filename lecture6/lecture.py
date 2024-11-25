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
update Amazon's database of how many items it has.

Let's start with our boilerplate code as always:
"""

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("OrderStreamProcessing").getOrCreate()
sc = spark.sparkContext

"""
Here's a toy example dataset which conveys the main idea:
"""

orders = [
    {"order_number": 1, "item": "Apple", "timestamp": "2024-11-24 10:00:00", "qty": 2},
    {"order_number": 2, "item": "Banana", "timestamp": "2024-11-24 10:01:00", "qty": 3},
    {"order_number": 3, "item": "Orange", "timestamp": "2024-11-24 10:02:00", "qty": 1},
    {"order_number": 4, "item": "Apple", "timestamp": "2024-11-24 10:03:00", "qty": 2},
    {"order_number": 5, "item": "Banana", "timestamp": "2024-11-24 10:04:00", "qty": 1},
    {"order_number": 6, "item": "Orange", "timestamp": "2024-11-24 10:05:00", "qty": 1},
]

"""
Let's look at the latency of the above in Spark:
"""

import time

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
        time.sleep(1)
        return order

    output = orders_rdd.flatMap(expand_order).map(process_order)

    # Ignore this for now
    # output.foreach(lambda x: print(f"Processed order: {x}"))

    # Return the result
    result = output.collect()
    print("Done processing orders")
    return result

# Uncomment to run
# result = process_orders_batch(orders)
# print(result)

"""
How to measure latency?

Formula is:

    (complete_time for item X - start_time for item X)

Sidenote: why NOT divide by the number of items?

    - What does latency mean for our real-world example?

OK, so let's apply our formula.
We have to pick an item X to measure latency for!
Let's do that below:

We can use time.time() to get the time.

Basically we have to consider where to insert:
start_time = time.time()
complete_time = time.time()
"""

# Uncomment
# result = process_orders_batch(orders)
# print(result)
# latency = TODO
# print(f"Latency: {latency} seconds")

"""
What happened?

(Think about it in terms of the real-world scenario)

What's the problem with the above code?

Main idea to fix it:
Try uncommenting the "output.foreach" line above that we ignored.
This is basicaly the first step to fixing our pipeline.
"""

"""
Upshots of this example:

Recap on latency:
- Latency = Response Time
- Latency can only be measured by focusing on a single item or row.
- Latency is not the same as 1 / Throughput
    + If it were, we wouldn't need two different words :)

A possibly helpful view:
- Throughput is about quantity: *how many* total orders were procesed (per hour, per day, etc.)
- Latency is about quality: *how fast* each individual order was processed.

Most important:
- To get good latency, we need to return each result as it is processed, instead of
  at the very end of job.

  We call this "stream processing" or "real-time processing", which is in contrast to
  "batch processing".

=== Q: Is stream processing always a good idea? ===

A:


"""

"""
=== Spark Streaming ===

Let's see a streaming example.

We need to decide where to get our input! Spark supports getting input from:
- Kafka (good production option)
- Files on a distributed file system (HDFS, S3)
- A network socket (basically a connection to some other worker process or network service)

We're looking for a toy example, so let's use a plain socket.

This will require us to open up another terminal and run the following command:

        nc -lk 9999

"""

# New imports
from pyspark.sql.functions import from_json, col, explode, expr
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
    parsed_df = order_stream.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))

    # Do some "processing"
    # We could put the equivalent of the flatMap from before
    # (Commenting this out for now)
    # expanded_orders = order_stream.withColumn(
    #     "expanded_items",
    #     expr("array_repeat(struct(order_number, item), qty)")
    # ).withColumn("item", explode("expanded_items.item")) \
    # .select("order_number", "item")

    # Let's just print the orders for now
    return parsed_df

# (Uncomment to run)
# # Set up the input stream using a local network socket
# order_stream = spark.readStream.format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()

# # Call the function
# out_stream = process_orders_stream(order_stream)

# # Print the output stream
# out = out_stream.writeStream.outputMode("append").format("console").start()

# # Start the computation
# out.awaitTermination()

"""
There are actually two streaming APIs in Spark,
the old DStream API and the newer Structured Streaming API.

Above uses the Structured Streaming API (which is more flexible and solves some problems with DStreams, I also personally found it better to work with on my machine.)

=== Time is Complicated ===

Final thing: in talking about latency, we constantly referred to time.
What is time, anyway?

Time is complicated!
Some optional but highly recommended reading:
https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca

I'd like you to know the following definitions of time:

- Real time
- System time
- Event time

System time can further be divided into:
- Ingress time
- Processing time
- Egress time
"""

"""
=== Exercises ===

1. Edit our streaming pipeline to measure each of the above measures of time.
What happens?

2. Edit our batch pipeline to measure each of the above measures of time.
"""
