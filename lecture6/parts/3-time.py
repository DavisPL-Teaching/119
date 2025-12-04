"""
Part 3: Time

=== Quick recap ===

- **Streaming pipelines** process each item as it arrives, without waiting for further items.

    + **Microbatching** is an optimization of streaming pipelines where we group items
      into small "batches" that we will process together,
      to help improve efficiency.

    + You can think of microbatching like a combination of streaming and batch processing.

- **Latency** is the response time from when an input enters to when it exits the pipeline.

Similarlities and differences from batch pipelines?

Most concepts from batch pipelines still apply to streaming pipelines:
  wide/narrow operators and partitioning.
  lazy/not lazy (we will not cover this aspect)

Differences: Because each item is processed as it arrives, latency is not equal
    to the running time of the entire batch.

=== Measuring time ===

In talking about latency, we constantly referred to time.

    latency = response time

    latency for item X = (exit time for item X) - (entrance time for item X)

When discussing progress in Spark Streaming, we saw how to use
time to grab and process "microbatches" of data.

    Using time to measure out microbatches is actually surprisingly complicated!

    What does it mean to wait for 5ms?

    Wait for 5ms, process the current batch,
    and I go back to the clock and I see that 7ms have now passed.
    Do I wait for 3 more ms? Or do I wait for 5 more ms?
    What if 20ms have passed?

The problem is:

    1. Time goes up as we are processing data (whether we want it to or not)

    2. Time has to be tied to some digital/computer notion of time.

        Our pipeline doesn't have access to the actual wall clock time in the room;
        so it has to use some synthetic "proxy" or digital notion of time to figure
        out how much time has ellapsed.

(Measuring time -- and thus, measuring progress in the system -- is
central to both of these discussions.)

Most commonly (so far in this class), we've used time.time() to get the time;
which is what we would refer to as "Operating System Time".

This is not quite the same as the true time according to a well calibrated clock on the
wall; for example, the OS time may be set wrong, or may be in a different time zone.

Time is complicated!

Where we're going - next time, we will explain a few of these different notions of time
with some examples,
and their relevance to stream processing pipelines and microbatching in these systems.

***** Where we ended for today *****

Some optional but highly recommended reading:
https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca

(scroll through a few of these)

Optional, but required if you want to implement software that relies on time.
"""

"""
December 3

=== Poll ===

https://forms.gle/Fov9LZ2arcLG6WUVA

A dataflow graph contains two nodes, a "map" node and a "filter" node:

(input dataset) -> (map) -> (filter)

The pipeline is evaluated as a streaming pipeline.

If the input dataset has 500 items, the map stage takes 1 ms per input item, and the filter stage takes 1 ms per input item, and map and filter are done in parallel, what is the latency of the pipeline in milliseconds?

Answer:

- This is a streaming pipeline, so one item comes in at a time.
- Takes 1 ms to do map, 1 ms to do filter, and we have to do these in order, so 2 ms total

Bonus question:
Would your answer change if the pipeline was based on microbatch sizes of 5 ms?

- we wait for 5ms for the microbatch -- on average, we wait 2.5ms per item
- we do 1ms for map
- we do 1ms for filer
- total latency
    = average of (end_time_item_X - start_time_item_X)
    = (2.5ms) + 1ms + 1ms = 4.5ms.

4.5 ms > 2ms, so we will wait longer on average (latency will increase).

This is always teh case - microbatch trades latency for throughput.
(Higher latency, but we get higher throughput in return.)
"""

"""
=== Different definitions of time ===

Unlike a batch pipeline, streaming pipelines use time to figure out which items
to process! (e.g., microbatching - wait for 5 ms)

But how do we measure time?

I'd like you to know the following definitions of time in general:

1. Real time (also known as "wall clock time")
    Time in the real world.
    Right now, it's 3:38pm (Pacific time) on December 3, 2025.
    Problem: technically speaking, your application does not have access to real time.
    Assuming your application does have access to the real time can lead to bugs
    in a distributed system.

In practice, systems only have access to one or more "synthetic" notions of time:

2. System time:

    System time is the time that is tracked a computer system,
    typically, your operating system.

    System time is generally kept up to date as much as possible - but this relies on the
    system having access to the internet and syncing the time, so sometimes it can fail to update.

    time.time() in Python returns OS system time.

    System time is not always equal to real time!
    It can be out of sync due to time zone changes, computer is reset by manufacturer, ...

3. Event time:

    Event time is a piece of structured data associated with input data to your pipeline.
    Users when submitting events include a time with that event.

    Imagine you have a Pandas or Spark DataFrame or any other tabular data
    Event time is just another column in your dataset.

    | User name | password hash | account creation |
    | Jane Doe  | xasdfasdf13415 | Dec 1, 2024 |

    Event time is treated as data.
    It has all of the problems that real world data has.
    - It could be faulty
    - It could be missing
    - We may need to validate to check for null values or extreme values (e.g., January 1, 1970 -
      "start of Unix time"
      an erroneous time that sometimes shows up due to systems not syncing the time correctly :-))
    - It requires validation to ensure it satisfies application requirements.
    - Queries or pipeline operators can refer to event time and use it to make certain computations.
    - In HW1, computed "year over year avg increase in population"
      That was actually using event time!
      The "year" field is just some piece of data that was given to us.

4. Logical time:

    Not even really time - just a logical counter in your program

    Last time we talked about microbatching strategies, and a suggested came up
    that we should batch every 10 items as one batch.

    That's logical time.

    Assign each item in your system an item number (index)

        First item = 1
        Second item = 2
        Third item = 3

    The "time" that the item occurs is the item #.

    Logical time doesn't correspond to real time at all, it's not really
    related to real time or system time,
    but it is much more reliable for the purposes of implementing a robust system.

    Systems use logical time internally to measure progress.

    Advanced: Logical time also gets more complicated than just integers; for example
    using vectors of integers (Vector Clocks - look up if interested)

=== Code example ===

Let's edit our streaming pipeline to log each notion of time.

Syntax we need to know:
    df.withColumn(...)

    current_timestamp()

    time.time()

New concepts:
    UDF = User Defined Function

In the interest of time I will probably
just show the final code and what it does.
"""

# Old imports
import time
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("OrderProcessing").getOrCreate()
sc = spark.sparkContext
from pyspark.sql.functions import array_repeat, from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# New imports
from pyspark.sql.functions import current_timestamp, udf, date_format

# Define the schema of the incoming JSON data
schema = StructType([
    StructField("order_number", IntegerType()),
    StructField("item", StringType()),
    StructField("timestamp", StringType()),
    StructField("qty", IntegerType())
])

### Time logging UDF

from datetime import datetime

def current_system_time():
    # Return the current system time
    # Raw timestamp:
    # return time.time()
    # Pretty print the output:
    # similar to time.time() but more readable
    readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return readable_time

time_udf = udf(current_system_time, StringType())

def log_time(stream, suffix):
    return (
        stream
        .withColumn(f"system_time_{suffix}", time_udf())
        .withColumn(f"spark_time_{suffix}", date_format(current_timestamp(), "yyyy-MM-dd HH:mm:ss"))
    )

### Delay UDF to make the computation take longer

def process_delay():
    # Simulate a difficult processing step by inserting a delay
    time.sleep(2)
    return "delay applied"

process_delay_udf = udf(process_delay, StringType())

def log_delay(stream):
    return stream.withColumn("delay", process_delay_udf())

def process_orders_stream_with_timing(order_stream):
    # Code from before
    df0 = order_stream.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))
    df1 = df0.select(
        col("parsed_value.order_number").alias("order_number"),
        col("parsed_value.item").alias("item"),
        col("parsed_value.timestamp").alias("timestamp"),
        col("parsed_value.qty").alias("qty")
    )

    # Uncomment to include
    df1 = log_time(df1, "start")

    df2 = df1.withColumn("order_numbers", array_repeat(col("order_number"), col("qty")))

    # Uncomment to include
    df3 = df2.select(explode(col("order_numbers")).alias("order_no"), col("item"), col("timestamp"), col("system_time_start"), col("spark_time_start"))

    # Uncomment to include
    df3 = log_delay(df3)

    # Uncomment to include
    df3 = log_time(df3, "end")

    # Return
    return df3

# (Uncomment to run)
# Remember to load up nc -lk 9999 before starting!
# order_stream = spark.readStream.format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()
# out_stream = process_orders_stream_with_timing(order_stream)
# out = out_stream.writeStream.outputMode("append").format("console").start()
# out.awaitTermination()

"""
Notes:

System timestamp differs between input and output

Everything in a microbatch has the same Spark timestamp!

This is how Spark tracks progress for a microbatch.

----------

Things to play with:

1. Comment/uncomment the lines for the time logging functions.

2. Comment/uncomment the lines to include the delay function.

3. Which columns correspond to which notion of time?

4. Can we add logical time to the pipeline?  Why or why not?

5. Can we add real time to the pipeline?  Why or why not?

6. Are some of the columns monotonic? Mark them.

7. Are some of the columns redundant? Remove them.

=== Discussion ===

Monotonic:

    A measure of time is called monotonic if whenever I call get_time() twice,
    and the results are x and y, it should be true that
        x <= y

Unfortunately this property is not always true.

Q: Which of 1-4 are guaranteed to be monotonic?

1. Real time: monotonic according to physics.

2. System time: not monotonic in general. Why?

    Answers?
    - Time got reset along the way? (Restarted the computer or rest it)
    - Time zones

        (Imagine you are doing the HW and get on a plane while measuring
         throughput and latency; when you land, the time zone is 3 hours different,
         and you get wrong values as a result)

    - You can just go into the settings and change the clock.

      What makes this problem in the real world is that servers will actually
      reset their clock and modify the time in order to synchronize times across
      machines.

      When clocks are synched, time could go forward in time or backward in time!

Q: In the context of a streaming application, which of the above do you think is useful?

A:
    OS time, event time, monotonic time.

As a general rule,
for queries on the data you should compute using event time,
but if you're implementing a real system under the hood, the implementation
should rely on things like system time and logical time to ensure progress
and to measure time within the system.

=== System time variants in a streaming system ===

In Spark Streaming, Spark uses system time internally to
measure and track progress within the pipeline.

Spark actually assigns a timestamp to each microbatch
and uses the timestamp throughout the pipeline.

We have seen these variants in the above code example:
- Input data timestamp - event time
- Spark timestamp - system time (at the start of the batch)
- Arrival time - system time (at the data item arrival)
- Exit time - system time (at the data item exit)
"""
