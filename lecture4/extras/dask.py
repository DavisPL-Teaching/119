"""
=== Dask: Parallelizing our code in Pandas (SKIP) ===

We don't want to parallelize our code by hand.
(why? See problems with concurrency from last week!)

Dask is a simple library that works quite well for parallelizing datasets
on a single machine as a drop-in replacement for Pandas.
"""

# conda install dask or pip3 install dask
import dask

def dask_example():
    # Example dataset
    df = dask.datasets.timeseries()

    # Dask is "lazy" -- it only generates data when you ask it to.
    # (More on laziness later).
    print(type(df))
    print(df.head(5))

    # Use a standard Pandas filter access
    df2 = df[df.y > 0]
    print(type(df2))
    print(df2.head(5))

    # Do a group by operation
    df3 = df2.groupby("name").x.mean()
    print(type(df3))
    print(df3.head(5))

    # Compute results -- this processes the whole dataframe
    print(df3.compute())

# If you just want parallelism on a single machine,
# Dask is a great lightweight solution.

# Uncomment to run.
# dask_example()
