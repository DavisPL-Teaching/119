"""
Part 4: End notes

=== Poll ===

This is the last poll!

What type of time corresponds to each of the following scenarios?

(Real time, event time, system time, logical time)

Select all that apply

https://forms.gle/NCXfDV4J3ySWiyiT6

=== Summary ===

We've seen:

- Streaming systems: differ from batch processing systems in that they process
  one item (or row) in your input at a time

- This is useful for "latency-critical" applications where you want, say, sub-second
  or sub-millisecond level respnose times

- Measuring latency at an individual item level:

    Recall formula for latency:

    (exit time item X) - (start time item X)

- Microbatching: an optimization that trades latency for higher throughput

    Microbatching can be based on different notions of time! Usually event time or system time

    Microbatching - still a streaming system!

- Time: Real, Event, System, Logical

    + Monotonic time

=== Discussion and Failure Cases ===

Streaming pipelines' (e.g., in Spark Streaming)
major advantage is better latency.

However, they have additional failure cases from their batch counterparts.
Let's cover a few of these:

- Out-of-order data (late arrivals)

- Clock drift and non-monotonic clocks

    (streaming system cares about time - batch prcoessing system didn't!)

- Too much data

.
.
.

Q: How do we deal with out-of-order data?

Q: How do we deal with clocks being wrong?

Q: How do we deal with too much data?

Q: What happens when our pipeline is overloaded with too much data, and the above techniques fail?
"""
