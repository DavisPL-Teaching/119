"""
Throughput and latency calculation example.

Throughput: Number of items processed per unit time
Latency: Time taken to process a single item
"""

from lecture import pipeline, get_life_expectancy_data

"""
Timeit:
https://docs.python.org/3/library/timeit.html

Library that allows us to measure the running time of a Python function

Example syntax:
timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
"""
import timeit

IN_FILE_THROUGHPUT = "life-expectancy.csv"
IN_FILE_LATENCY = "life-expectancy-row1.csv"
OUT_FILE = "output.csv"

def throughput(num_runs):
    """
    Measure the throughput of our example pipeline, in data items per second.

    We need to run it a bunch of times to get an accurate number,
    that's why we're taking a num_runs parameter and passing it to
    timeit

    Updated formula if we run multiple times
        N = input dataset size
        T = total running time
        num_runs = number of times I ran the pipeline
    Throughput =
        N / (T / num_runs)
    """

    print(f"Measuring throughput over {num_runs} runs...")

    # Number of items
    num_items = len(get_life_expectancy_data(IN_FILE_THROUGHPUT))

    # ^^ Notice I'm doing this cmoputation outside of the actual measurement
    # (timeit) code - if you start measuring things as you're computing
    # them, this leads to distortion of the results
    # (Kind of like Quantum Mechanics - if you measure it, it changes)

    # Function to run the pipeline
    def f():
        pipeline(IN_FILE_THROUGHPUT, "output.csv")

    # Measure execution time
    execution_time = timeit.timeit(f, number=num_runs)

    # Print and return throughput
    # Display to the nearest integer
    throughput = num_items * num_runs / execution_time
    print(f"Throughput: {int(throughput)} items/second")
    return throughput

def latency(num_runs):
    """
    Measure the average latency of our example pipeline, in seconds.

    (In today's poll: we saw an example where we measured latency
     not just with one input row)

    *Key point:*
    We use a one-row version of the pipeline to measure latency
    """

    print(f"Measuring latency over {num_runs} runs...")

    # Function to run the pipeline
    def f():
        pipeline(IN_FILE_LATENCY, "output.csv")

    # Measure execution time
    execution_time = timeit.timeit(f, number=num_runs)

    # Print and return latency (in milliseconds)
    # Display to 5 decimal places
    latency = execution_time / num_runs * 1000
    print(f"Latency: {latency:.5f} ms")
    return latency

if __name__ == "__main__":
    throughput(1000)
    latency(1000)

"""
Observations?

~4.1M items/second
    Pandas is very fast!
    (We are just doing max/min/avg, probably things would slow
     down for something more complicated)

Somewhat stable across runs - this is because we run the
    pipeline always multiple times

    (Lesson: always run multiple times for best practice)

Is throughput always constant with the number of input items?
    No!

    (Try deleting items from input dataset - what happens?)

Latency: about ~0.7 ms

Latency != 1 / Throughput

Latency is much greater for a dataset with one row.
"""
