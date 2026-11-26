"""
Part 6: End notes

Latency and throughput, revisited
and
Disadvantages of Spark

=== Latency and throughput ===

So, we know how to build distributed pipelines.

The **only** change from a sequential pipeline is that
tasks work over scalable collection types, instead of regular data types.
Tasks are then interpreted as operators over the scalable collections.
In other words, data parallelism comes for free!

Scalable collections are a good way to think about parallel AND/OR distributed
pipelines. Operators/tasks can be:
- lazy or not lazy (how they are evaluated)
- wide or narrow (how data is partitioned).

=== Limitations ===

There is however one main limitation of what we have done so far!

Spark and MapReduce are optimized for throughput.

It's what we call a *batch processing engine.* That means?

A: It processes all the data "as one batch", or as "one job",
then comes back with an answer

But doesn't optimizing for throughput always optimize for latency? Not necessarily!

Recall, restaurant analogy:

- Throughput is how many orders we were able to process per hour.

- Latency is how long *one* person waits for their order.

Spark batches everything up
(recall - queueing up "transformations" lazily, then computing/returning all results on an "action")

This is like taking everyone's order for an hour, then queueing up everything at once.
This has good and bad aspects!

    good: we know exactly how much of each ingredient to use (every
          operation is done maximally efficiently)
    bad: each customer has to wait for the entire hour!

So in Spark,
we always get the worst possible latency, in fact we get the maximum latency
on each individual item. We don't get some results sooner and some results later.

Grouping together items (via lazy transformations) helps optimize the pipeline, but it
*doesn't* necessarily help get results as soon as possible when they're needed.
(in fact it does the opposite - remember laziness poll/example)

That's why there is a tradeoff between throughput and latency.

=== Summary: where we are going next ===

So that's where we're going next:
talking about applications where you might want your pipeline to respond in real time to data that
is coming in.

Data processing for "low-latency" applications is known as "streaming" or "stream processing"
(also synonymous with "real-time" data processing)

And systems/frameworks for this case are known as "stream processing systems" (or frameworks).

Aim for: typically, sub-second, sometimes milliseconds latency.

    "To achieve low latency, a system must be able to perform
    message processing without having a costly storage operation in
    the critical processing path...messages should be processed “in-stream” as
    they fly by."

    From "The 8 Requirements of Real-Time Stream Processing":
    Mike Stonebraker, Ugur Çetintemel, and Stan Zdonik
    https://cs.brown.edu/~ugur/8rulesSigRec.pdf

We'll use a different API in Spark called Spark Structured Streaming.
"""
