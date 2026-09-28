"""
Part 2: Extract, Transform, Load (ETL)

===Continuing our example ===
"""

# Copied from Part 1
data = {
    "User": ["Alice", "Alice", "Charlie"],
    "Website": ["Google", "Reddit", "Wikipedia"],
    "Time spent (seconds)": [120, 300, 240],
}

# As dataframe:
import pandas as pd
df = pd.DataFrame(data)

print(data)
print(df)

"""
Let's think about this example from a more abstract perspective.

What are the main "abstract" components of the data processing job in this scenario?

A:

- A dataset
- Processing steps
- Some kind of user-facing output

Three components!

=== "Extract, Transform, Load" model (ETL) ===

What is an ETL job?

- **Extract:** Load in some data from an input source
    (e.g., CSV file, spreadsheet, a database)

- **Transform:** Do some processing on the data

- **Load:** (Sometimes a confusing name)
  we save the output to an output source.
    (e.g. CSV file, spreadsheet, a database)

It turns out that a *lot* of data processing work in practice
boils down to carrying out these three steps (often repeatedly),
for various data sources and loading targets.

=== Questions ===

Which of the above might be consider Extract, Transform, and Load?

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
.
.

Can we restructure the code to make the delineation into the three
stages explicit?

"""

# Uncomment to run
# # Some logic to compute the maximum length of time website sessions
# u = df["User"]
# w = df["Website"]
# t = df["Time spent (seconds)"]
# # Max of t
# max = t.max()
# # Filter
# max_websites = df[df["Time spent (seconds)"] == max]

# # Let's print our data and save it to a file
# with open("save.txt", "w") as f:
#     print(max_websites, file=f)

"""
First step: can we abstract this as an ETL job?
"""

def extract():
    # TODO
    raise NotImplementedError

    # return df

def transform(df):
    raise NotImplementedError

    # u = df["User"]
    # w = df["Website"]
    # t = df["Time spent (seconds)"]
    # # Max of t
    # max = t.max()
    # # Filter
    # # This syntax in Pandas for filtering rows
    # # df[colname]
    # # df[row filter] (row filter is some sort of Boolean condition)
    # return df[df["Time spent (seconds)"] == max]

def load(df):
    raise NotImplementedError
    # Save the dataframe somewhere
    # with open("save.txt", "w") as f:
    #     print(df, file=f)

# Uncomment to run
# df = extract() # get the input
# df = transform(df) # process the input
# print(df) # printing (optional)
# load(df) # save the new data.

"""
We have a working pipeline!
But this may seem rather silly ... why rewrite the pipeline
to achieve the same behavior?

=== Advantages of abstraction ===

Q: why abstract the steps into Python functions?

(instead of just using a plain script, Jupyter notebook, etc.)

ETL steps are not done just once!

A possible development lifecycle:

- Exploration time:
  Thinking about my data, thinking about what I might
  want to build, exploring insights
  -> there is no pipeline yet, we're just exploring

- Development time:
  Building or developing a working pipeline
  -> a script or abstracted functions would both work!

- Production time:
  Deploying my pipeline & reusing it for various purposes
  (e.g., I want to run it like 5x per day)
  -> pipeline needs to be reused multiple times
  -> we could even think about more stages, like
     maintaining the pipeline as separate items after production time.

In general, for this class we will think most about production time,
because we are ultimately interested in being able to fully automate and
maintain pipelines (not just one-off scripts).

Some of you may have used tools like Jupyter notebooks;
(very good for exploration time!)

I will generally be working directly in Python in this course.

I want you to get used to thinking of processing directly "as code",
good abstractions via functions and classes, and follow good practices like
unit tests, etc. to integrate the code into a larger project.

Abstractions means we can test the code:
"""

import pytest

# Unit test example
# @pytest.mark.skip # uncomment to skip this test
def test_extract():
    df = extract()
    # What do we want to test here?
    # Test that the result has the data type we expect
    assert type(df) is not None
    assert type(df) == pd.DataFrame
    # check the dimensions (I'll skip this)
    # Sanity check - check that the values are the correct type!

# @pytest.mark.skip # uncomment to skip this test
def test_transform():
    df = extract()
    df = transform(df)
    # check that there is exactly one output
    assert df.count().values[0] == 1

# Run:
# - pytest lecture.py

"""
Discussion Question / Poll:

https://forms.gle/REBtUGxyzHQgH73V6

1. Can you think of any scenario where test_extract() will fail?

2. Will test_transform() always pass, no matter the input data set?

===== Recap =====

- Want: a general model of data processing pipelines

- First-cut model: Extract Transform Load (ETL)

    Any data process job can be split into three stages,
    input, processing, output
    (extract, transform, load)

Next we will introduce a better model for general data processing pipelines - Dataflow Graphs.

"""
