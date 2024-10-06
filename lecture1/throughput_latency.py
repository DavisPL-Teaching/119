"""
Throughput and latency calculation example.

Throughput: Number of items processed per unit time
Latency: Time taken to process a single item
"""

from lecture import pipeline, get_life_expectancy_data

import timeit

IN_FILE_THROUGHPUT = "life-expectancy.csv"
IN_FILE_LATENCY = "life-expectancy-row1.csv"
OUT_FILE = "output.csv"

def throughput(num_runs):
    """
    Measure the throughput of our example pipeline, in data items per second.
    """

    print(f"Measuring throughput over {num_runs} runs...")

    # Number of items
    num_items = len(get_life_expectancy_data(IN_FILE_THROUGHPUT))

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
    Measure the latency of our example pipeline, in seconds.
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
