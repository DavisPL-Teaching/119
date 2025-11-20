"""
Part 2:
Spark Streaming and Microbatching

=== Poll ===

Which of the following are most likely application scenarios for which latency matters?

.
.
.

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
# order_stream = spark.readStream.format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()

# # Call the function
# out_stream = process_orders_stream(order_stream)

# # Print the output stream and run the computation
# out = out_stream.writeStream.outputMode("append").format("console").start()
# out.awaitTermination()

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
"""
