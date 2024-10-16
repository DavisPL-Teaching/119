"""
Lecture 3: Data operators in Pandas

=== What is an operator? ===

Operators include any function with input data and output data.
(These are the "processing" part of our 3-stage data pipelines.)

(Contrast with:
- input, which provide raw datasets into your pipeline
- generators, which produce data from nothing
- output, some sort of display to the user or export to storage
- consumers, which consume data without producing anything.)

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
We also won't cover stastical analysis tasks like time series analysis,
regression, supervised learning, unsupervised learning and data mining, etc.
(these should have been covered in many of your other DS courses),
but note that these all have analogs in Pandas.

=== Look around, get help, do stuff model ===

Just as in the shell lecture, the look around, get help, do stuff model
is useful for understanding a new Python class...

We'll keep this in mind as we go through.

=== Getting Started ===

Let's start by getting a dataset.
We'll use another dataset from Our World in Data, this time on population.
"""

print("Welcome to lecture 3.")

import pandas as pd

def load_data():
    return pd.read_csv('population.csv')

"""
=== Informational commands ===

So, we've loaded a data frame, what's the first step?

We have already seen how to view the data (to stdout),
first 5 rows, last 5 rows.

Q: What other things might we want to do
to get a "feel" for a dataset?

Your answers:
- Get the column names
- Get the shape
- Get the column types
- Get the count of the data
- Check for null values

My answers (we will cover):

- Get the column names and types
  .columns
  .info()
  - includes non-null count, types

- Get the shape
  .shape
    (59177, 4)
    - I have 59177 rows, 4 columns.

  This is analagous to the shape of Numpy arrays.

  - DataFrames are like 2D Numpy arrays
  - Series ojbects are like 1D Numpy arrays
    You can confirm this by doing x = df["Year"], x.shape.

  We can also get the shape of a single column or row,
  or even the column headers (for example).

  .columns.shape
  ["column1"].shape
  ["column1", "column2"].shape
  .iloc[0].shape

===== Recap =====

We finished the Shell lecture
We introduced what a data operator is (contrast with: generators, consumers)
We began a tour of the DataFrame class and available data operators
We started to talk about the first steps that you might want to do
when you initially load in a dataset to Pandas ("looking around")
operators.

========================================

=== Wed Oct 16 ==

Lessons for today:

- Ways to look around a dataset when first loading it in

- We can use relational operators on data frames

- Mutability

- Going beyond relational operators

=== Continuing ===

Continuing: things to do when first opening a new dataset

- Get a random sample

  .sample(5)

- Get the number of unique values in each column

  .nunique()
  .nunique(axis=1)

- See how we are doing on missing values

  .isnull()
  .notnull()

  What do we discover?
"""

# TODO

"""
=== Documentation and getting help ===

After we have gotten a handle on the dataset, our next step
is to get help and documentation on what methods are available
to us.

- The Pandas documentation is very good. I recommend:
  https://pandas.pydata.org/docs/reference/index.html#api

- As an "introductory guide" I especially recommend the comparison
  with SQL. We will be following this gudie:
  https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html

In addition, Python has built-in ways to get help about a class.

I will mention some that I have found particularly useful:

- dir(df)
- help(pd.DataFrame)
- help(df)

Other miscellaneous:
- help("modules")
- set(locals())
- set(globals())
"""

def print_variables_in_scope():
    for x in locals():
        print(f"Local: {x}")
    for x in globals():
        print(f"Global: {x}")

# print_variables_in_scope()

"""
So what should we do?

Let's start with relational algebra operators.

=== Relational operator equivalents ===

Recall relational operators: select, project, join, group-by.

Project:
We have already seen how to select columns by name.
- Keep only certain columns
"""

"""
Select:
- Filter rows based on a condition

We can index into a DataFrame with a boolean array!
"""

"""
Join:
- Combine two DataFrames based on a common column

df.join(df, lsuffix="1", rsuffix="2")

df.join(other, on="Year")
"""

"""
Group-by:

    df.groupby("Year").groups[2023]
    df.groupby("Year").get_group(2023)
    df.groupby("Year").sum()
    df.groupby("Year").count()
    df.groupby("Year")["Population (historical)"].sum()
    df.groupby("Year")["Population (historical)"].mean()
"""

"""
=== Mutation vs. immutability ===

One important distinction in Python is between operators
that mutate in-place, vs. those that return a new object.
This can be a major source of errors!

In general in Pandas, you should assume that operators
return a new DataFrame, unless it can be done in an obvious
way in-place
  (e.g., modifying a single cell or column name).

Also, when modifying in place, we often have to explicitly call
a method which has an in-place version.

Example:

  .loc[row, col] = value

Let's see some examples of this.

  .insert(2, "foo2", [3, 4, 5, 6, 6])

"""

"""
Some operations have both in-place and non-in-place versions.

  .rename(columns={"foo": "bar"}, inplace=True)

"""

"""
===== A more general view =====

Structure data vs general data processing?

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
