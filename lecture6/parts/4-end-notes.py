"""
Part 4: End notes

=== Poll ===

What type of time corresponds to each of the following scenarios?

.
.
.

=== Measuring latency ===

Which type of time should we use to measure latency?

Recall formula for latency:

    (exit time item X) - (start time item X)

=== Discussion and Failure Cases ===

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
