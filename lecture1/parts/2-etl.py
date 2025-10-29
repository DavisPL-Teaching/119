"""
Monday, September 29

Part 2: Extract, Transform, Load (ETL)

=== REMINDER: FOLLOWING ALONG ===

https://github.com/DavisPL-Teaching/119

- Open terminal (Cmd+Space Terminal on Mac)

- `git clone <paste repository link>`

    + if you have already cloned, do a `git stash` or `git reset .`

- `git pull`

- **Why use the command line?**

  Short answer: it's an important skill!

  Long answer:
  I do require learning how to use the command line for this course.
  More in Lecture 2.
  GUI tools only work if someone else already wrote them (they used the command line to write the tool)
  You'll find that it is SUPER helpful to know the basics of the command line for stuff like installing software, managing dependencies, and debugging why installation didn't work.
  The command prompt is how all internal commands work on your computer - and it's an important skill for data engineering in practice.

=== Continuing our example ===

Recall from last time:

- Want: a general model of data processing pipelines

- First-cut model: Extract Transform Load (ETL)

    Any data process job can be split into three stages,
    input, processing, output
    (extract, transform, load)

Example on finding popular websites:
"""

# (Re-copying from above)
data = {
    "User": ["Alice", "Alice", "Charlie"],
    "Website": ["Google", "Reddit", "Wikipedia"],
    "Time spent (seconds)": [120, 300, 240],
}
df = pd.DataFrame(data)

# Some logic to compute the maximum length of time website sessions
u = df["User"]
w = df["Website"]
t = df["Time spent (seconds)"]
# Max of t
max = t.max()
# Filter
max_websites = df[df["Time spent (seconds)"] == max]

# Let's print our data and save it to a file
with open("save.txt", "w") as f:
    print(max_websites, file=f)

"""
Running the code

It can be useful to have open a Python shell while developing Python code.

There are two ways to run Python code from the command line:
- python3 lecture.py
- python3 -i lecture.py

Let's try both.
"""

"""
First step: can we abstract this as an ETL job?
"""

def extract():
    data = {
        "User": ["Alice", "Alice", "Charlie"],
        "Website": ["Google", "Reddit", "Wikipedia"],
        "Time spent (seconds)": [120, 300, 240],
    }
    df = pd.DataFrame(data)
    return df

def transform(df):
    u = df["User"]
    w = df["Website"]
    t = df["Time spent (seconds)"]
    # Max of t
    max = t.max()
    # Filter
    # This syntax in Pandas for filtering rows
    # df[colname]
    # df[row filter] (row filter is some sort of Boolean condition)
    return df[df["Time spent (seconds)"] == max]

def load(df):
    # Save the dataframe somewhere
    with open("save.txt", "w") as f:
        print(df, file=f)

# Uncomment to run
df = extract() # get the input
df = transform(df) # process the input
# print(df) # printing (optional)
load(df) # save the new data.

"""
We have a working pipeline!
But this may seem rather silly ... why rewrite the pipeline
to achieve the same behavior?

=== Tangent: advantages of abstraction ===

Q: why abstract the steps into Python functions?

(instead of just using a plain script)

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
while excellent tools,
I will generally be working directly in Python in this course.

Reasons: I want to get used to thinking of processing directly "as code",
good abstractions via functions and classes, and follow good practices like
unit tests, etc. to integrate the code into a larger project.

Abstractions mean we can test the code:
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

1. Can you think of any scenario where test_extract() will fail?

2. Will test_transform() always pass, no matter the input data set?

https://forms.gle/j99n5ZN7jsJ6gHB2A

********** Where we ended for September 29 **********
"""
