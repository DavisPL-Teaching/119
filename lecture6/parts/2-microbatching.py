"""
Part 2:
Spark Streaming and Microbatching

=== Poll ===

Which of the following are most likely application scenarios for which latency is a primary concern?

.
.
.

https://forms.gle/Le4NZTDEujzcqmg47

=== Spark Streaming ===

In particular: Structured Streaming
Structured = using relational and SQL abstractions
Structured Streaming syntax is similar (often almost identical) to Spark DataFrames

There's an analogy going on here!
Batch processing application using DataFrames <---> Streaming application using Structured Streaming

Let's see our streaming example in more detail.

(We demoed this example last time)
"""

# Old imports
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("OrderProcessing").getOrCreate()
sc = spark.sparkContext

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
- Files on a distributed file system (HDFS (Hadoop File system), S3)
- A network socket (basically a connection to some other worker process or network service)

We're looking for a toy example, so let's use a plain socket.

This will require us to open up another terminal and run the following command:

        nc -lk 9999

"""

# We need an input (source)

# (Uncomment to run)
# Set up the input stream using a local network socket
# One of the ways to get input - from a network socket
order_stream = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Call the function
out_stream = process_orders_stream(order_stream)

# We need an output (sink)

# Print the output stream and run the computation
out = out_stream.writeStream.outputMode("append").format("console").start()

# Run the pipeline

# Run until the connection closes.
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

To process a streaming pipeline, Spark groups several recent orders into something
called a "microbatch", and processes that all at once.

(Side note: this isn't how all streaming frameworks work, but this is
the main idea behind how Spark Streaming works.)

Why does Spark do this?

- If you process every item one at a time, you get minimum latency!

  Every user will get their order processed right away.

  But, throughput will suck.

  - We never benefit from parallelism (because we're never doing more than one order at the same time)

  - We never benefit from techniques like vectorization (we can't put multiple orders into vector operations on a CPU or GPU)

    (Recall: turning operatinos into vector or matrix multiplications is often faster and
     I can only do that if I have many rows that look the same)

So: by grouping items into these "microbatches", Spark hopes to still provide good latency (by processing microbatches frequently, e.g., every half a second) but at the same time benefit from
throughput optimizations, e.g., parallelism and vectorization.

That leads to an interesting question: how do we determine the microbatches?

- There is a tension here; the smaller the batches, the better the latency;
  but the worse the throughput!

Possible ways?

1. Wait 0.5 seconds, collect all items during that second and group it into a batch
2. Set a limit on the number of items per batch (e.g. 100), once you get 100
   items, close the batch
3. Set a limit on the number of items, OR wait for a 2 second timeout

Some observations:

- Suggestion 1 will always result in latency < 0.5 s, but batches may be small

- Suggestion 2 has a serious problem, on a non-busy day, imagine there's only 1 Amazon
  user.

  Amazon user submits their order -> we wait for the other 99 orders to come in (which
  never happens, or takes hours)

  Our one user will never get their results.

- Suggestion 3 fixes the problem with suggestion 2, by imposing a timeout.

  Suggestion 3 tries to achieve large batch sizes, but caps out at a certain maximum;
  latency will always be at most 2 seconds (often smaller if there are many orders).

=== Another way of thinking about this ===

It comes down to a question of "time" and how to measure progress.

All distributed systems measure progress by enforcing some notion of "time"

Suggestion #1 measures time in terms of the operating system clock
    (e.g., time.time())

Suggestions #2 measures time in terms of how many items arrive in the pipeline,
and uses that to decide when to move forward.

    This is related to something called "logical time", and we will cover it in
    the following part 3.

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
"""
