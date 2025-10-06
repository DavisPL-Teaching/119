"""
Lecture 1: Introduction to data processing pipelines

This lecture will cover the required background for the rest of the course.

Please bear with us if you have already seen some of this material before!
I will use the polls to get a sense of your prior background and adjust the pacing accordingly.

=== Note on materials from prior iteration of the course ===

The GitHub repository contains the lecture notes from a prior iteration of the course (Fall 2024).
You are welcome to look ahead of the notes, but please note that most content will change as I revise each lecture.
I will generally post the revised lecture before and after each class period.

**Changes from last year:**
I plan to skip or condense Lecture 3 (Pandas) based on feedback and your prior background.
I will also cover some Pandas in Lecture 1.
(I will confirm this after the responses to HW0.)

=== Poll ===

Today's poll is to help me understand the overall class background in command line/Git.
(I will also ask about your background in more detail on HW0.)

https://forms.gle/2eYFVpxT1Q8JJRaMA

^^ find the link in the lecture notes on GitHub

Piazza -> GitHub -> lecture1 -> lecture.py
https://piazza.com/

=== Following along with the lectures ===

Try this!

1. You will need to have Git installed (typically installed with Xcode on Mac, or with Git for Windows). Follow the guide here:

    https://www.atlassian.com/git/tutorials/install-git

    Feel free to work on this as I am talking and to get help from your neighbors.
    I can help with any issues after class.

    (Note on Mac: you can probably also just `brew install git`)

2. You will also need to create an account on GitHub and log in.

3. Go to: https://github.com/DavisPL-Teaching/119

4. If that's all set up, then click the green "Code" button, click "SSH", and click to copy the command:

    git@github.com:DavisPL-Teaching/119.git

5. Open a terminal and type:

    git clone git@github.com:DavisPL-Teaching/119.git

6. Type `ls`.

    You should see a new folder called "119" in your home folder. This contains the lecture notes and source files for the class.

7. Type `cd `119/lecture1`, then type `ls`.

8. Lastly type `python3 lecture.py`. You should see the message below.
"""

print("Hello, ECS 119!")

"""
Let's see if that worked!

If some step above didn't work, you may be missing some of the software we
need installed. Please complete HW0 first and then let us know if you
are still having issues.

=== The basics ===

I will introduce the class through a basic model of what a data processing
pipeline is, that we will use throughout the class.

We will also see:
- Constraints that data processing pipelines have to satisfy
- How they interact with one another
- Sneak peak of some future topics covered in the class.

To answer these questions, we need a basic model of "data processing pipeline" - Dataflow Graphs.

Recall discussion question from last lecture:

EXAMPLE:
You have compiled a spreadsheet of website traffic data for various popular websites (Google, Instagram, chatGPT, Reddit, Wikipedia, etc.). You have a dataset of user sessions, each together with time spent, login sessions, and click-through rates. You want to put together an app which identifies trends in website popularity, duration of user visits, and popular website categories over time.

What are the main "abstract" components of the pipeline in this scenario?

- A dataset
- Processing steps
- Some kind of user-facing output

closely related:
"Extract, Transform, Load" model (ETL)

What is an ETL job?

- **Extract:** Load in some data from an input source
    (e.g., CSV file, spreadsheet, a database)

- **Transform:** Do some processing on the data

- **Load:** (perhaps a confusing name)
  we save the output to an output source.
    (e.g. CSV file, spreadsheet, a database)

"""

data = {
    "User": ["Alice", "Alice", "Charlie"],
    "Website": ["Google", "Reddit", "Wikipedia"],
    "Time spent (seconds)": [120, 300, 240],
}

# As dataframe:
import pandas as pd
df = pd.DataFrame(data)

# print(data)
# print(df)

"""
Recap:

- We spent some time getting everyone up to speed:
    After completing HW0, you should be able to follow along with the lectures
    locally on your laptop device

- We started to introduce the abstract model that we will use throughout the class
  for data processing pipelines - this will be called the Dataflow Graph model

- We began by introducing a simpler concept called Extract, Transform, Load (ETL).

***** Where we ended for Friday *****

===============================================

Monday, September 29

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

"""
=================================

Friday, October 3

From ETL to Dataflow Graphs.

=== Poll ===

Which of the following are most likely advantages of writing or rewriting
a data processing pipeline as well-structured software (separated into modules, classes, and functions)?

https://forms.gle/akNYHe8SY1CSU5KT9

=== Dataflow graphs ===

We can view all of the above steps as something called a dataflow graph.

ETL jobs can be thought of visually like this:

    (Extract) -> (Transform) -> (Load)

This is a Directed Acyclic Graph (DAG)

A graph is set a nodes and a set of edges

    ()       () -> ()
        () -> ()

Nodes = points
Edges = arrows between points

We're going to generalize the ETL model to allow an arbitrary
number of nodes and edges.

Q: What are the nodes? What are the edges?

    - Nodes:
        Each node is a function that takes input data and produces output data.

        Such a function is called an *operator.*

        In Python:
"""

# example: operator with 3 inputs:
def stage(input1, input2, input3):
    # do some processing
    # return the output
    return output

# example: operator with 0 inputs:
def stage():
    # do some processing
    # return the output
    return output

"""
    - Edges:
        Edges are datasets!
        They can either be:
        - individual rows of data, or
        - multiple rows of data...

    - More specifically, we draw an edge
        from a node (A) to a node (B) if
        the operator B directly uses the output of operator (A).

In our previous example?

(1) Extract = loading the set of websites sessions into a Pandas dataframe
    + Input: None (because we loaded from a file)
    + Output: A Pandas DataFrame

(2) Transform = taking in the Pandas DataFrame and returning the session with the
  maximum time spent
    + Input: The pandas DataFrame from the Extract stage
    + Output: the maximum session

(3) Load = taking the maximum session and saving that to a file (in our case, save.txt)
    + Input: the maximum session from the Transform stage
    + Output: None (because we saved to a file)

Graph:

    (1) -> (2) -> (3)

Questions:

- Why is there an edge from (1) to (2)?
    Because the Transform stage uses the output from the Extract stage

- Why is there NOT an edge from (2) to (1)?
    Stage (1) doesn't use the output from stage (2)

- Why is there NOT an edge from (1) to (3)?
    Stage (3) doesn't directly use the output from stage (1).

The graph is **acyclic,** meaning it does not have loops.

    (This is why it's a "directed acyclic graph" (DAG)).

- (Why can we assume this?)
    + It doesn't appear to make sense for stage (1) to use stage (2)'s output,
      and stage (2) to use stage (1)'s output.
    + Generalizations of this are possible, but we will not get into this now.

=== Q: Do all data processing pipelines look like series of stages? ===

A "very complicated" data processing job:
a long series of stages

    (1) -> (2) -> (3) -> (4) -> (5) -> (6) -> ... -> (10)

But not all data processing dataflow graphs have this form!
Let's do a quick example

Suppose that in addition to the maximum session, we want the minimum session.
"""

def stage1():
    data = {
        "User": ["Alice", "Alice", "Charlie"],
        "Website": ["Google", "Reddit", "Wikipedia"],
        "Time spent (seconds)": [120, 300, 240],
    }
    df = pd.DataFrame(data)
    return df

def stage2(df):
    t = df["Time spent (seconds)"]
    # Max of t
    max = t.max()
    # Filter
    # This syntax in Pandas for filtering rows
    # df[colname]
    # df[row filter] (row filter is some sort of Boolean condition)
    return df[df["Time spent (seconds)"] == max]

def stage3(df):
    # Save the dataframe somewhere
    with open("save.txt", "w") as f:
        print(df, file=f)

# New stage:
# Also compute the minimum session
def stage4(df):
    t = df["Time spent (seconds)"]
    min = t.min()
    return df[df["Time spent (seconds)"] == min]

# Finally, print the output from stage4
def stage5(df):
    # print: the .head() of the dataframe, which will give you the first
    # few rows.
    print(df.head())

# Try running the pipeline
df1 = stage1()
df2 = stage2(df1)
df3 = stage3(df2) # uses output from stage 2
df4 = stage4(df1)
df5 = stage5(df4) # uses output from stage 4

"""
As a dataflow graph:

    (1) -> (2) -> (3)
        -> (4) -> (5)

This is our dataflow graph for this example.

Seems like a simple idea, but this can be done for any data processing pipeline!

We will see that this is a very powerful abstraction.

=== Why is this useful? ===

- We'll use this to think about development, testing, and validation
- We'll use this to think about parallelism
- We'll use this to think about performance.
"""

"""
A slightly more realistic example

What I want to practice:
1. Thinking about the stages involved in a data processing computation as separate stages
    (List out all of the data processing stages)
2. Writing down the dataflow graph
3. Translating that to Python code using PySpark by writing a separate Python function
   for each stage

Let's consider how to write a minimal data processing pipeline
as a more structured software pipeline.

First thing we need is a dataset!

Useful sites:
- https://ourworldindata.org/data
- https://datasetsearch.research.google.com/
- sklearn: https://scikit-learn.org/stable/api/sklearn.datasets.html

The dataset we are going to use:
    life-expectancy.csv

We will also use Pandas, as we have been using:

Useful tutorial on Pandas:
https://pandas.pydata.org/docs/user_guide/10min.html
https://pandas.pydata.org/docs/user_guide/indexing.html
"""

# Step 1: Getting a data source
# creating a DataFrame
# DataFrame is just a table: it has rows and columns, and importantly,
# each column has a type (all items in the column must share the same
# type, e.g., string, number, etc.)
df = pd.read_csv("life-expectancy.csv")

# To play around with our dataset:
# python3 -i lecture.py

# We find that our data contains:
# - country, country code, year, life expectancy

# What should we compute about this data?

# A simple example:
min_year = df["Year"].min()
max_year = df["Year"].max()
print("Minimum year: ", min_year)
print("Maximum year: ", max_year)
avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
print("Average life expectancy: ", avg)

# Tangent:
# We can do all of the above with df.describe()

# Save the output
out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
out.to_csv("output.csv", index=False)

"""
Q for next time: rewrite this as a Dataflow graph using the steps above

=== Recap ===

We learned that ETL jobs are a special case of dataflow graphs,
where we have a set of nodes (operators/stages) and edges (which are drawn when the output
of one operator or stage depends on the output of the previous operator or stage)

Revisiting the steps above:
1. Write down all the stages in our pipeline
2. Draw a dataflow graph (one node per stage)
3. Implement the code (one Python function per stage)

We have done 1 and (sort of) 3, we will do 2 at the start of class next time.

********* Where we ended for today **********

===============================================================

Monday, October 6

On Friday, I introduced the concept of dataflow graphs.
Recall:
-

=== Practice with dataflow graphs ===

At the end of last class period, we introduced a dataset for life expectancy.
We saw a simple data pipeline for this dataset.
Let's separate it into stages as follows:

(read) = load the CSV input
(max) = compute the max
(min) = compute the min
(avg) = compute the avg
(print) = Print the max, min, and avg
(save) = Save the max, min, and avg to a file


=== Discussion Question and Poll ===

Suppose we draw a dataflow graph with the above nodes.

1. What edges will the graph have?
  (draw/write all edges)

2. Give an example of two stages A and B, where the output for B depends on A, but there is no edges from A to B.

https://forms.gle/6FB5hhwKpokTHhit9

Key points:


=== A few more things ===

A couple of more definitions:

- A stage B *depends on* a stage A if...

point: The dataflow graph reveals exactly which computations depend on which others!

- A *source* is...

- A *sink* is ...

point: The dataflow graph reveals exactly where the I/O operations are for your pipeline.

So there are three types of nodes:


In Python:
We could write each node as a stage, as we have been doing before.

Let's just write one example, in the interest of time
"""

def max_stage(df):
    raise NotImplementedError

"""
Reminders for why this helps:

- Better code re-use
- Better ability to write unit tests
- Separation of concerns between different features, developers, or development efforts
- Makes the software easier to maintain (or modify later)
- Makes the software easier to debug

Zooming in on one of these...
(pick one)

Q: How is this better than the ETL model?
"""

"""
=== Data validation ===

We will talk more about data validation at some point, most likely as part of Lecture 3.
(See failures.py for a further discussion)

Where in a pipeline is data validation most important?

Validation in a dataflow graph:
we may view each edge as having some "constraints" that are validated by the previous stage,
and assumed by the next.

=== Performance ===

Let's touch on one other advantage of looking at dataflow graphs:
we can use them to think about performance.

For traditional programs, there are two notions of performance that matter:

For data processing programs?


- Throughput

    What is throughput?

    Most pipelines run slower the more input items you have!

    - Often linear: the more input items, the longer it will take to run

    So we might want to know how fast the pipeline runs, *per input row or input item.*

    So it's useful to think about the time per input item.

    Throughput is the inverse of this:
    Definition / formula:
        (Number of input items) / (Total running time).

Let's take our pipeline and measure the total running time & the throughput.

see throughput_latency.py
"""

def get_life_expectancy_data(filename):
    pass

# Wrap up our pipeline - as a single function!
# You will also do this on the HW to measure performance.
def pipeline(input_file, output_file):
    # TODO: update
    # df = get_life_expectancy_data(input_file)
    # stats_summary = load_statistics(df)
    # stats_summary.save_to_file(output_file)
    pass

# Use the timeit library -- library that allows us to measure the running
# time of a Python function
import timeit

def f():
    pipeline("life-expectancy.csv", "output.csv")

# timeit.timeit(f, number=100)
# We see a linear behavior!
# 100 times: 0.35s
# 1000 times: 3.28s
# 10000 times: 33.4s
# Running time is roughly linear in the size of the input!

def measure_throughput():

    # Get the number of input items
    # Hardcoded
    num_input_items = 20755

    # Get the number of runs
    # Hardcoded
    num_runs = 1000

    execution_time = timeit.timeit(f, number=num_runs)

    print(f"Execution time for {num_runs}: {execution_time}")

    print(f"Execution time per input run: {execution_time / num_runs}")

    ans = execution_time / (num_runs * num_input_items)
    print(f"Execution time per input run, per input data item (1/throughput): {ans}")

    # The actual number we want: throughput
    print(f"Throughput: {1 / ans} items/second")

    # Answer: about 6,000,000 items (or rows) per second!
    # Pandas is very fast.

"""
- Latency

    What is latency?

    Sometimes, we care about not just the time it takes to run the pipeline...
    but the time on each specific input item.

    Why?
    - Imagine crawling the web at Google.
      The overall time to crawl the entire web is...
      It might take a long time to update ALL websites.
      But I might wonder,
      what is the time it takes from when I update my website
          ucdavis-ecs119.com
      to when this gets factored into Google's search results.

      This "individual level" measure of time is called latency.

    *Tricky point*

    For the pipelines we have been writing, the latency is the same as the running time of the entire pipeline!

    Why?

- Memory usage

Let's measure the performance of our toy pipeline.

Timeit:
https://docs.python.org/3/library/timeit.html

Example syntax:
timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
"""

def measure_latency(pipeline):
    raise NotImplementedError

def measure_memory_usage(pipeline):
    # There are ways to do this in Python through external libraries.
    # We will cover this later.

    raise NotImplementedError

"""
Some formulas

    N = number of input items
    T = running time of the pipeline

    Throughput
        =

    Latency (for the pipelines we have considered so far)
        =
"""

"""
=== Overview of the rest of the course ===

Overview of the schedule (tentative), posted at:
https://github.com/DavisPL-Teaching/119/blob/main/schedule.md

=== Closing quotes ===

Fundamental theorem of computer science:

    "Every problem in computer science can be solved by another layer of abstraction."

    - Based on a statement attributed to Butler Lampson
    https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering

A dataflow graph is an abstraction (why?), but it is a very useful one.
It will help put all problems about data processing into context and help us understand how
to develop, understand, profile, and maintain data processing jobs.

It will provide a common framework for the rest of the course.
"""

# Main function: the default thing that you run when running a program.

# print("Hello from outside of main function")

if __name__ == "__main__":
    # Insert code here that we want to be run by default when the
    # program is executed.

    # print("Hello from inside of main function")

    # What we can do: add additional code here
    # to test various functions.
    # Simple & convenient way to test out your code.

    # Call our pipeline
    # pipeline("life-expectancy.csv", "output.csv")

    pass

# NB: If importing lecture.py as
# a library, the main function (above) doesn't get run.
# If running it directly from the terminal,
# the main function does get run.
# See test file: main_test.py
