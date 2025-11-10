
"""
=== Cut material ===

===== Understanding latency (abstract) =====
(review if you are interested in a more abstract view)

Why isn't optimizing latency the same as optimizing for throughput?

First of all, what is latency?
Imagine this. I have 10M inputs, my pipeline processes 1M inputs/sec (pretty well parallelized.

    (input)   --- (process)
      10M        1M / sec

Latency is always about response time.
To have a latency you have to know what change or input you're making to the system,
and what result you want to observe -- the latency is the difference (in time)
between the two.

Latency is always measured in seconds; it's not a time "per item" or dividing the total time by number
of items (that doesn't tell us how long it took to see a response for each individual item!)

So, what's the latency if I just put 1 item into the pipeline?
(That is, I run on an input of just 1 item, and wait for a response to come back)?

We can't say! We don't know for example, whether the
1M inputs/sec means all 1M are processed in parallel, and they all take 1 second,
or the 1M inputs/sec means that
it's really 100K inputs every tenth of a second at a time.

This is why:
    Latency DOES NOT = 1 / throughput
in general and it's also why optimizing for throughput doesn't always benefit latency
(or vice versa).
We will get to this more in the next lecture.
"""
