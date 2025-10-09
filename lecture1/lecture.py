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
    To build a dataflow graph, we divide our pipeline into a series of "stages"
To build the graph, we draw:
    - One node per stage of the pipeline
    - An edge from node A to B (A -> B) if node B directly uses the output of node A.

=== Practice with dataflow graphs ===

At the end of last class period, we introduced a dataset for life expectancy.
We saw a simple data pipeline for this dataset.
Let's separate it into stages as follows:

(read) = load the CSV input
(max) = compute the max
(min) = compute the min
(avg) = compute the avg
(print) = Print the max, min, and avg
(save) = Save the max, min, and avg in a dataframe to a file

=== Discussion Question and Poll ===

Suppose we draw a dataflow graph with the above nodes.

1. What edges will the graph have?
  (draw/write all edges)

2. Give an example of two stages A and B, where the output for B depends on A, but there is no edge from A to B.

https://forms.gle/6FB5hhwKpokTHhit9

Answer:

           -> (max) ----|--> (print)
    (read) -> (min) ----|
           -> (avg) ----|--> (save)

Key points:

    Two "independent" computations will not have an edge one way or the other
    (printing produces output to the terminal, save produces output to a file,
     neither one is used by the other)

    We can read off dependence information from the graph! If there is a path
    from A to B, then B depends (either directly or indirectly) on A.

    What graph we get depends on the precise details of our stages.
    Ex.: if we load the input three different times, once for the max, once for the min,
    once for the avg (and this is listed in our description of the computation),
    we would get a different graph with 8 nodes instead of 6.

    In order to draw this thing, we should refer to the particular way that we wrote out
    our computation.

=== A few more things ===

A couple of more definitions:

- A stage B *depends on* a stage A if...

    there is a path from A to B

    point: The dataflow graph reveals exactly which computations depend on which others!

- A *source* is a node without any input edges
    (typically, a node which loads data from an external source)
    (corresponds to the E stage of the ETL model)

- A *sink* is a node without any output edges
    (typically, a node which saves data to an external source)
    (corresponds to the L stage of the ETL model)

- A small correction from last time: let's define
  an *operator* is any node that is not a source or a sink.
  Operators take input data, and produce output data
    (corresponds to the T stage of the ETL model)

Points:

    Every node in the dataflow graph is one of the above 3 types

    The dataflow graph reveals exactly where the I/O operations are for your pipeline.

We can use the dataflow graph to reveal (visually and conceptually) many useful features of our pipeline.

In Python:
We could write each node as a stage, as we have been doing before.

Let's just write one example, in the interest of time
"""

def max_stage(df):
    return df["Year"].max()

"""
Reminders for why this helps:

(Maybe it's overkill for a one-liner example like this)

- Better code re-use
- Better ability to write unit tests
- Separation of concerns between different features, developers, or development efforts
- Makes the software easier to maintain (or modify later)
- Makes the software easier to debug

Zooming in on one of these...
(pick one)

Q: How does this correspond to ETL model?

ETL is basically a dataflow graph with 3 nodes.
"""

"""
=== Data validation ===

We will talk more about data validation at some point, most likely as part of Lecture 3.
(See failures.py for a further discussion)

Where in a pipeline is data validation most important?

(There is more than one place where validation could help, but what's the most obvious place to start?)

A: Right before transformations
    (After sources)

Why?
    - Most common problem: malformed input
    - I might want to validate that all of my rows have the type that I'm expecting before
      I move to any further processing.
    - This might even simplify or speed up the later stages as in those stages I'm allowed
      to assume that the data is well-formed.

NB: You can validate at any point in the graph. (And it can be useful!)

Validation in a dataflow graph:
we may view each edge as having some "constraints" that are validated by the previous stage,
and assumed by the next.

=== Performance ===

Let's touch on one other thing that we can do with dataflow graphs:
we can use them to think about performance.

Dataflow graphs are basically the "data processing" equivalent of programs.

For traditional programs, there are two notions of performance that matter:

- Runtime or time complexity
- Memory usage or space complexity

For data processing programs?

We'll care about the most:
- Running time corresponds to: Throughput & Latency
- Memory usage: you can also measure, we'll talk briefly about ways of thinking about this.

**********

Recap:

We reviewed the definition of dataflow graph
- divided into sources, operators, and sinks
- def of when to draw an edge

We practiced drawing dataflow graphs

We used dataflow graphs to explore various features of a data processing computation

We argued that analagous to regular computer programs for the traditional computing world,
    dataflow graphs are the right notion of computer programs for the data processing world.

********** where we ended for today **********

================================================

October 8

Let's talk about performance!

But first, the poll.

=== Poll / discussion question ===

True or false:

1. Two different ways of writing the same overall computation can have two different dataflow graphs.

2. Operators always take longer to run than sources and sinks.

3. Typically, every node in a dataflow graph takes the same amount of time to run.

https://forms.gle/wAAyXqbJaCkEzyZP9

Correct answers: T, F, F

For 1:
Max and min?
Say I have a dataset in a dataframe df with fields x and y
And I want to do df["x"].max()
and df["x"].min()
"""

df = load_input_dataset()
min = df["x"].min()
max = df["x"].max()

"""
Dataflow graph with nodes
(load_input_dataset) node
(max) node
(min) node

       --> (max)
(load)
       --> (min)

       --> (min)
(load)
       --> (max)

Same graph! Has the same nodes, and has the same edges.

This is actually a great example of a slightly different phenomenon:

1b. Two different ways of writing the same overall computation can have *the same* dataflow graph.

A different example?

If one operator does depend on the other, BUT the answer doesn't depend on the order, you could rearrange them to get an example where
- the overall computation was the same, but
- the dataflow graph was different

example:
- Get row with values x, y, and z
- First, we compute a = x + y
- Then we compute a + z = x + y + z.

OR, we could
- First, compute b = x + z
- Then we compute b + y = x + y + z.

We could get the same answer in two different ways.

And in this example, the dataflow graph is also different:

(input) -> (compute x + y) => (compute a + z)
(input) -> (compute x + z) => (compute b + z).

An easier example is .describe() from last time.
"""

"""
Last time, we reviewed the notions of performance for traditional programs.

There's two types of performance that matter: time & space.

For data processing programs?

===== Running time for data processing programs =====

Running time has two analogs. We will see how these are importantly different!

- Throughput

    What is throughput?

    Most pipelines run slower the more input items you have!

    Think about how long it will take to run an application that
    processes a dataset of university rankings, and finds the top 10
    universities by ranking.

    You will find that if measuring the running time of such an application,
    a single variable dominates ...
    the number of rows in your dataset.

    Example:
    1000 rows => 1 ms
    10,000 rows => ~10 ms
    100,000 rows => ~100 ms

    - Often linear: the more input items, the longer it will take to run

    So it makes sense to measure the performance in a way that takes this
    into account:

        running time = (number of input items) * (running time per item)

        (running time per item) = (running time) / (number of input items)

    Throughput is the inverse of this:
    Definition / formula:
        (Number of input items) / (Total running time).

    Intuitively: how many rows my pipeline is capable of processing,
    per unit time

    There's many real-world examples of this concept:

        -> the number of electrons passing through a wire per second

        -> the number of drops of water passing through a stream per second

        -> the number of orders processed by a restaurant per hour

    "number of things done per unit time"

Is this the only way to measure performance?

We also care about the individual level view: how long it takes to process
a *specific* item or order.

We also might measure, for an individual order, how long it takes for
results for that order to come out of our pipeline.

    Latency =
    (time at which output is produced) - (time at which input is received)

This is called latency.

It almost seems like we've defined the same thing twice?

But these are not the same.
Simplest way to see this is that we might process more than one item at
the same time.

Ex:
    Restaurant processes 60 orders per hour

    Scenario I:
        Process 5 orders every 5 minutes, get those done, and move on to
        the next batch

    Scenario II:
        Process 1 order every 1 minute, get it done, and then move on to
        the next order.

In either case, at the end of the hour, I've processed all 60 orders!

Throughput in Scenario I? In Scenario II?
    I:
        Throughput = (Number of items processed) / (Total running time)

        60 orders / 60 minutes = 1 order / minute.
    II:
        Throughput = (Number of items processed) / (Total running time)

        60 orders / 60 minutes = 1 order / minute

What about latency?

    I:
        (time at which output is produced) - (time at which input is received)

        = roughly 5 minutes

    II:
        (time at which output is produced) - (time at which input is received)

        = roughly 1 minutes

Both measures of running time at a "per item" or "per row" level,
but they can be very different.

It is NOT always the case that Throughput = 1 / Latency
or that Throughput and Latency are directly correlated (or inversely correlated).

===== Recap =====

We talked about how computations are represented as dataflow graphs
to illustrate some important points:
- The same computation (computed in different ways) can have two different dataflow graphs
- The same computation (computed in different ways) could have two of the same dataflow graph

We introduced throughput + latency
- Restaurant analogy
- We saw formulas for each
- Both measures of performance in terms of running time at an "individual row" level, but throughput is an aggregate measure and latency is viewed at the level of an individual row.

********** Where we ended for today **********

October 10

Recap from last time:

Throughput:

Latency:

Discussion question:

A health company's servers process 12,000 medical records per day.
The medical records come in at a uniform rate between 9am and 9pm every day (1,000 records per hour).
The company's servers submit the records to a back-end service that collects them throughout the hour, and then
processes them at the end of each hour to update a central database.

What is the throughput of the pipeline?

What number would best describe the *average latency* of the pipeline?
Describe the justification for your answer.

https://forms.gle/AFL2SrBr5MhwVV3h7
"""

"""
...

Let's see an example

We need a pipeline so that we can measure the total running time & the throughput.

I've taken the pipeline from earlier for country data and rewritten it below.

see throughput_latency.py
"""

def get_life_expectancy_data(filename):
    return pd.read_csv(filename)

# Wrap up our pipeline - as a single function!
# You will do a similar thing on the HW to measure performance.
def pipeline(input_file, output_file):
    df = get_life_expectancy_data(input_file)
    min_year = df["Year"].min()
    max_year = df["Year"].max()
    print("Minimum year: ", min_year)
    print("Maximum year: ", max_year)
    avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
    print("Average life expectancy: ", avg)
    # Save the output
    out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
    out.to_csv(output_file, index=False)

# SEE throughput_latency.py.

import timeit

def f():
    pipeline("life-expectancy.csv", "output.csv")

"""
=== Latency (additional notes - SKIP) ===

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

Let's measure the performance of our toy pipeline.
"""

"""
=== Formulas for reference ===

    N = number of input items
    T = running time of the pipeline for N items

    Throughput
        =

    Latency
        (for a one-item pipeline)
        (we will consider generalizations of this later in the course)
        =

When running a pipeline multiple times (to get an average)


"""

"""
=== Memory usage ===

What about the equivalent of memory usage?

I will not discuss this in detail at this point, but will offer a few important ideas:

- Input size:

- Output size:

- Window size:

- Distributed notions: Number of machines, number of addresses on each machine ...

Which of the above is most useful?

How does memory relate to running time?
For traditional programs?
For data processing programs?
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
