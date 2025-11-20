"""
Part 6: End notes

Latency and throughput, revisited
and
Disadvantages of Spark

=== Latency and throughput ===

So, we know how to build distributed pipelines.

The **only** change from a sequential pipline is that
tasks work over scalable collection types, instead of regular data types.
Tasks are then interpreted as operators over the scalable collections.
In other words, data parallelism comes for free!

Scalable collections are a good way to think about parallel AND/OR distributed
pipelines. Operators/tasks can be:
- lazy or not lazy (how they are evaluated)
- wide or narrow (how data is partitioned)

But there is just one problem with what we have so far :)
Spark and MapReduce are optimized for throughput.
It's what we call a *batch processing engine.* That means?

A: It processes all the data, then comes back with an answer

But doesn't optimizing for throughput always optimize for latency? Not necessarily!

Let's talk a little bit about latency...

=== Understanding latency (intuitive) ===

A more intuitive real-world example:
imagine a restaurant that has to process lots of orders.

- Throughput is how many orders we were able to process per hour.

- Latency is how long *one* person waits for their order.

Some of you wrote on the midterm: throughput == 1 / latency

These are not the same! Why not? Two extreme cases:

----

Suppose the restuarant processes 10 orders over the course of being open for 1 hour

Throughput =
    10 orders / hour

Latency is not the same as 1 / throughput! Two extreme cases:

1.
    Every customer waits for the entire hour!
    Every customer submitted their order at the start of the hour,
    and got it back at the end.

    Latency = 1 hour
        (customers are not very happy)

2.
    One order submitted every 6 minutes,
    and completed 6 minutes later.

    Latency = 6 minutes
        (customers are happy)

    (A more abstract example of this is given below in the "Understanding latency (abstract)" section below.)

Throughput is the same in both cases!
10 events / 1 hour

(The first scenario is similar to a parallel execution,
the second scenario more similar to a sequential execution.)

The other formula which is not true:

    Latency != total time / number of orders
    True in the second scenario but not in the first scenario.

How can we visualize this?

    (Draw a timeline from 0 to 1 hour and draw a line for each order)

So, optimizing latency can look very different from optimizing throughput.

In a batch processing framework like Spark,
it waits until we ask, and then collects *all* results at once!
So we always get the worst possible latency, in fact we get the maximum latency
on each individual item. We don't get some results sooner and some results later.

Grouping together items (via lazy transformations) helps optimize the pipeline, but it
*doesn't* necessarily help get results as soon as possible when they're needed.
(Remember: laziness poll/example)
That's why there is a tradeoff between throughput and latency.

    "To achieve low latency, a system must be able to perform
    message processing without having a costly storage operation in
    the critical processing path...messages should be processed “in-stream” as
    they fly by."

    From "The 8 Requirements of Real-Time Stream Processing":
    Mike Stonebraker, Ugur Çetintemel, and Stan Zdonik
    https://cs.brown.edu/~ugur/8rulesSigRec.pdf

Another term for the applications that require low latency requirements (typically, sub-second, sometimes
milliseconds) is "real-time" applications or "streaming" applications.

=== Summary: disadvantages of Spark ===

So that's where we're going next,
talking about applications where you might want your pipeline to respond in real time to data that
is coming in.
We'll use a different API in Spark called Spark Structured Streaming.
"""
