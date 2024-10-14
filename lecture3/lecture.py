"""
Lecture 3: Data operators in Pandas

=== What is an operator? ===

Operators include any function with input data and output data.
(These are the "processing" part of our 3-stage data pipelines.)

(Contrast with: generators, which produce data from nothing,
and consumers, which consume data without producing anything.)

=== Learning Objectives ===

This lecture will be structured as a guide of various operators
available in the Pandas library.

- We are already familiar with the basic DataFrame object.

- I will also assume familiarity with DB/SQL operations: select,
  project, join, and group-by.
  (Spoiler: these all have analogs in Pandas.)

- We will tour validation, selection, and manipulation of data on
  DataFrames, starting with operators which correspond to
  relational operators, and moving to more complex ones.

=== Non-objectives ===

We won't go into detail about data wrangling or cleaning at this stage
(e.g., handling missing data, normalization, different encodings like
one-hot encoding, etc.)
I've also decided to postpone topics like web scraping and API access
for a later lecture.
We also won't cover advanced stastical operations like time series analysis,
machine learning, etc. though they all have analogs in Pandas.

=== Getting Started ===

Let's start by getting a dataset.
We'll use another dataset from Our World in Data, this time on population.
"""

import pandas as pd

def load_data():
    return pd.read_csv('population.csv')

"""
=== Informational commands ===

We have already seen how to view the data (to stdout),
first 5 rows, last 5 rows.

Q: What other things might we want to do
to get a "feel" for a dataset?

Your answers:

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

My answers (we will cover):

- Get the column names and types
- Get the shape
- Get a random sample
- Get the number of unique values in each column
- See how we are doing on missing values

"""

# TODO

"""
=== Relational operator equivalents ===

Recall relational operators: select, project, join, group-by.

Starting with Project:
- Keep only certain columns
"""

"""
Select:
- Filter rows based on a condition
"""

"""
Join:
- Combine two DataFrames based on a common column
"""

"""
===== A more general view =====

Not all data is structured nicely like Pandas DataFrames.
It is sometimes useful to think in more general terms
about data processing. A common way is to talk about operators
falling into roughly the following categories:

- Map: apply a function to each element
- Filter: keep only some elements
- Join: combine two datasets in some way (not always by a common column)
- Group: combine elements into groups
- Sort: order elements in some way
- Reduce: combine elements into a single value

Other interesting operators:
- Inspect (very useful for debugging)

Some other interesting ones (which we won't cover until the parallel lecture):
- "Partition by" key
- Round robin
- Union

Some operators get more interesting with time-series:
- Window: look at a subset of elements at a time
- Lag, re-timestamp, delay: look at elements at different times
- Delta: look at differences between timestamps
- Interpolate: fill in missing values in a time series
"""
