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

df = load_data()

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

Lesson plan for today:

- (continued) Ways to look around a dataset when first loading it in
  & getting help

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
- help(df)
- help(pd.DataFrame)

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

- You'll notice that this doesn't actually modify the data frame

Often, you might just modify by doing:

  df = df[["columns", "that", "I", "actually", "want"]].

  df[[]] -- creates an empty dataframe with no columns

Select:
- Filter rows based on a condition

We can index into a DataFrame with a boolean array!

- df[df["Year"] == 2023]

- df[df["Code"].notnull()]

Example to clean the data:

- df_countries = df[(df["Code"].notnull()) & (df["Entity"] != "World")]

=== Recap ===

We saw how to get a random sample

Random sampling (& looking at .info() and nonnull values) can help
identify anomalies or biases in the data that we might need to clean

We looked at how to do select and project (SELECT A FROM B WHERE C queries)
in the SQL world using Data Frame equivalents.

Next time:

- We'll get into Join and other more interesting operations!

========================================================

=== Fri Oct 18 ===

So far, we have seen:

- Data frames are 2D arrays of data.
  Rows are labled by integer index (by default)
  Columns are labeled by name.

- SQL equivalents:
  SELECT FROM = access columns
  WHERE = access rows by Boolean array

Plan for today:

- Continue our general overview of available data operators
  + not just in Pandas, but in other data processing frameworks!
    (SQL, R, Spark, etc.)

- Focus in on some common gotchas:
  null values, duplicate values,
  mutability, and vectorization

Let's start with another simple example:

Ex.:
- Define a DataFrame for an employee database with 3 employees.

- Use SELECT WHERE to get the employees with a salary over $100,000.
"""

employees = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Salary": [2_000, 20_000, 200_000],
    "Age": [25, 35, 45],
})

employees_over_100000 = employees[employees["Salary"] > 100000]

"""
We've seen select, project, now join!

Review:
- There are many types of join! What are a few?
  + Left join
  + Outer join
  + Inner join
  + Right join

(not cover)
  + Self join
  + Cross join

Pandas supports two main forms of join:

Merge:
Confusingly, "merge" is used for an actual (relational) join.
Combine two DataFrames based on a common column:

  df1.merge(df2)
  df1.merge(df2, how="outer")

Ex.: Let's define a table for the employee locations
and join with our original employee data.
"""

locations = pd.DataFrame({
    "Name": ["Charlie", "Bob", "Alice"],
    "Location": ["NYC", "SFBA", "SFBA"],
})

print(employees.merge(locations))

"""
Join:
We can also join on index (often more efficient if it fits your use case)

  df1.join(df2, lsuffix="1", rsuffix="2")

  Joins by index.
"""

"""
How can different joins lead to different semantics?

Ex. 1: Define two employees with the same name
Ex. 2: Define one employee with a missing location
Ex. 3: Define one employee with a missing name
"""

employees2 = pd.DataFrame({
    "Name": ["Alice", "Alice", "Bob"],
    "Salary": [2_000, 20_000, 200_000],
    "Age": [25, 35, 45],
})

locations2 = pd.DataFrame({
    "Name": ["Alice", "Alice", "Bob"],
    "Location": ["NYC", "SFBA", "SFBA"],
})

employees3 = pd.DataFrame({
    "Name": ["Alice", "Alice", "Bob", "Charlie"],
    "Salary": [2_000, 20_000, 200_000, 2_000_000],
    "Age": [25, 35, 45, 60],
})

locations3 = pd.DataFrame({
    "Name": ["Bob", "Charlie", "Delphina"],
    "Location": ["NYC", "SFBA", "SFBA"],
})

print(employees3.merge(locations3, how="inner"))
print(employees3.merge(locations3, how="left"))
print(employees3.merge(locations3, how="right"))
print(employees3.merge(locations3, how="outer"))

"""
Group-by:

    df.groupby("Year").groups[2023]
        # return indices in group 2023
    df.groupby("Year").get_group(2023)
        # return the actual table of items in group 2023

    (BTW: equality:
      == does element-wise comparison
      .equals compares the whole table
    )

    df.groupby("Year").sum()
      more reasonable thing to do:
      df[["Year", "Population (historical)"]].groupby("Year").sum()

    df.groupby("Year").count()
    df.groupby("Year")["Population (historical)"].sum()
    df.groupby("Year")["Population (historical)"].mean()
"""

"""
=== Common gotchas! ===

Some common gotchas in Pandas:

- Null values (in join/merge)
- Duplicate values (in join/merge)
- Indexing (iloc vs. loc -- keys vs. indices)

  loc: how to access rows and row, column pairs by key
  iloc: how to access rows and row, column pairs by index

Why can iloc be misleading?

  - integer row number doesn't always correspond to logical key

  - Use loc to get the row(s) by key, iloc to get the row by row index.

double_table.iloc[1, 1] -- row 1, column 1
double_table.loc[1, "Salary"] -- row key 1, column key Salary
"""

pd.concat([employees, employees])
#       Name  Salary  Age
# 0    Alice    2000   25
# 1      Bob   20000   35
# 2  Charlie  200000   45
# 0    Alice    2000   25
# 1      Bob   20000   35
# 2  Charlie  200000   45

"""
Recap of what we covered today:
- We've finished informally proving that Pandas data frames can be used
  for everything SQL can be used for
- And they also support Numpy-style operations (like indexing by row, col number)

What we'll continue with  next time:
Two important gotchas in terms of the design:
- Mutability
- Vectorization

=======================================

Skipped the rest of the file for time.
Please feel free to review on your own!

=======================================

=== Mutability ===

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

Exercise:

1. Define a view of a dataframe (by using a select where)
and try to modify a value in it. What happens?

2. Use .concat to create a new dataframe.
   What happens to the original values?

  pd.concat(df1, df2)

  (Concat is another gotcha!)

"""

"""
=== Vectorization ===

What is vectorization?

Exercise: Using the population data, define a new row for
the next year (year + 1).

Then define the same thing by using a for loop
over the entries of the data frame.
What happens?
"""

"""
===== A more general view (beyond Pandas) =====

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
