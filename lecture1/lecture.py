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

Q: What are the nodes? What are the edges?

    - Nodes:

    - Edges:

In our previous example?



It's a flow chart (directed graph) of input sources,
processing stages (called "operators"), and outputs.

An edge is drawn from A to B if...

Questions:

- Why is there an edge from (1) to (2)?
- Why is there NOT an edge from (2) to (1)?
- Why is there NOT an edge from (1) to (3)?

The graph is **acyclic,** meanin it does not have loops.

- (Why can we assume this?)

- (Generalizing)

Vertex types?

Edge types?

Why is this useful?

- We'll use this to think about development, testing, and validation
- We'll use this to think about parallelism
- We'll use this to think about performance.
"""

"""
A slightly more realistic example

Let's consider how to write a minimal data processing pipeline
as a more structured software pipeline.

Step 1: Getting a data source

Step 2: Do some processing

Stage 3. Save the output

Useful sites:
- https://ourworldindata.org/data
- https://datasetsearch.research.google.com/
- sklearn: https://scikit-learn.org/stable/api/sklearn.datasets.html

Useful tutorial on Pandas:
https://pandas.pydata.org/docs/user_guide/10min.html
https://pandas.pydata.org/docs/user_guide/indexing.html
"""

# Step 1: Getting a data source
# creating a DataFrame
# DataFrame is just a table: it has rows and columns, and importantly,
# each column has a type (all items in the column must share the same
# type, e.g., string, number, etc.)
# df = pd.read_csv("life-expectancy.csv")

# Step 2: Do some processing
# min_year = df["Year"].min()
# max_year = df["Year"].max()
# print("Minimum year: ", min_year)
# print("Maximum year: ", max_year)
# avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
# print("Average life expectancy: ", avg)

# How can we write this as different dataflow nodes?

# Tangent:
# We can do all of the above with df.describe()

# Step 3: save the output
# out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
# out.to_csv("output.csv", index=False)
# Do this above

"""
Let's revisit our criteria from today's in-class poll. How does this help?
"""

# - Better code re-use

# - Will speed up the development of a one-off script

# - Better ability to write unit tests

# - Separation of concerns between different features, developers, or development efforts

# - Makes the software easier to maintain (or modify later)

#  - Makes the software easier to debug

"""
=== Failures and risks ===

Failures and risks are problems
which might invalidate our pipeline (wrong results)
or cause it to misbehave (crash or worse).

What could go wrong in our pipeline above?
Let's go through each stage at a time:

1. Input stage

What could go wrong here?

- Malformed data and type mismatches
- Wrong data
- Missing data
- Private data
"""

"""
Problem: input data could be malformed
"""

# Exercise 4: Insert a syntax error by adding an extra comma into the CSV file. What happens?

# A: that row gets shifted over by one
# All data in each column is now misaligned;
# some columns contain a mix of year and life expectancy data.

# Exercise 5: Insert a row with a value that is not a number. What happens?

# A: changing the year on just one entry to a string,
# the "Year" field turned into a string field.

# Reminder about dataframes: every column has a uniform
# type. (Integer, string, real/float value, etc.)

# Take home point: even a single mislabeled or
# malformed row can mess up the entire DataFrame

# Solutions?

# - be careful about input data (get your data from
# a good source and ensure that it's well formed)

# - validation: write and run unit tests to check
#   check that the input data has the properties we
#   want.

# e.g.: write a test_year function that goes through
# the year column and checks that we have integers.

"""
Problem: input data could be wrong
"""

# Example:
# Code with correct input data:
# avg. 61.61799192059744
# Code with incorrect input data:
# avg.: 48242.7791579047

# Exercise 6: Delete a country or add a new country. What happens?

# Deleting a country:
# 61.67449487559832 instead of 61.61799192059744
# (very slightly different)

# Solutions?

# Put extra effort into validating your data!

"""
Discussion questions:
- If we download multiple versions of this data
  from different sources (for example, from Wikipedia, from GitHub,
  etc.) are they likely to have the same countries? Why or why not?

- What can be done to help validate our data has the right set
  of countries?

- How might choosing a different set of countries affect the
  app we are using?

Recap from today:

- Python main functions (ways to run code: python3 lecture.py (main function), python3 -i lecture.py (main function + interactive), pytest lecture.py to run unit tests)
- what can go wrong in a pipeline?
- input data issues & validation.

===============================================================

=== Friday, Oct 4 ===

Following along: git stash, git pull

=== Poll ===

1. Which of the following are common problems with input data that you might encounter in the real world and in industry?

- (poll options cut)

2. How many countries are there in the world?

Common answers:

- 193: UN Members
- 195: UN Members + Observers
- 197: UN Members + Observers + Widely recognized
- 200-300something: if including all partially recognized countries or territories.

As we saw before, our dataset happens to have 261.
- e.g.: our dataset did not include all countries with some form of
  limited recognition, e.g. Somaliland
  but it would include the 193, 195, or 197 above.

Further resources:

- https://en.wikipedia.org/wiki/List_of_states_with_limited_recognition

- CGP Grey: How many countries are there? https://www.youtube.com/watch?v=4AivEQmfPpk

In any dataset in the real world, it is common for there to be some
subjective inclusion criteria or measurement choices.

"""

"""
2. Processing stage

What could go wrong here?

- Software bugs -- pipeline is not correct (gives the wrong answer)
- Performance bugs -- pipeline is correct but is slow
- Nondeterminism -- pipelines to produce different answers on different runs

    This is actually very common in the data processing world!
    - e.g.: your pipeline may be a stream of data and every time you run
    it you are running on a different snapshot, or "window" of the data
    - e.g.: your pipeline measures something in real time, such as timing
    - a calculation that requires a random subset of the data (e.g.,
      statistical random sample)
    - Neural network?
    - Running a neural network or large language model with different versions
      (e.g., different version of GPT every time you call the GPT API)
    - ML model with stochastic components
    - Due to parallel and distributed computing
        If you decide to parallelize your pipeline, and you do it incorrectly,
        depending on the order in which different operations complete you
        might get a different answer.

"""

"""
3. Output stage

What could go wrong here?

- System errors and exceptions
- Output formatting
- Readability
- Usability

Often output might be: saving to a file or saving to a database, or even
saving data to a cloud framework or cloud provider;
and all of three of these cases could fail.
e.g. error: you don't have permissions to the file; file already exists;
not enough memory on the machine/cloud instance; etc.

Summary: whenever saving output, there is the possibility that the save operation
might fail

Output formatting: make sure to use a good library!
Things like Pandas will help here -- formatting requirements already solved

When displaying output directly to the user:
- Are you displaying the most relevant information?
- Are you displaying too much information?
- Are you displaying too little information?
- Are you displaying confusing/incomprehensible information?

e.g.: displaying 10 items we might have a different strategy than if
we want to display 10,000

example: review dataframe display function
    - dataframe: display header row, first 5 rows, last 5 rows
    - shrink the window size ==> fields get replaced by "..."

There are some exercises at the bottom of the file.
"""

"""
=======================================================================
=======================================================================
=======================================================================

Prior materiral from Fall 2024 follows.

=======================================================================
=======================================================================

=== Monday, September 30 ===

(See README.md for announcements and plan.)

=== Poll ===

1. Which stage do you think is likely to be the most computationally intensive part of a data processing pipeline?

2. Which stage do you think is likely to present the biggest opportunity for failure cases, including crashes, ethical concerns or bias, or unexpected/wrong/faulty data?
"""

"""
===============================================================

"""

# (Finishing up)
# Reasons to think of data processing pipelines as software:

# - Collaborative development
#   Why is the above code design better for collaborative development?

# - Performance optimization
#   (More on this shortly)

# - In general: anticipating things that could go wrong
#   (this point is a good transition to the next section)

"""
=== Main function ===

Last time, we used python3 -i lecture.py to run
the code interactively.

Let's look at another common way to test out our Python code
by putting a basic pipeline into a main function at the
bottom of the file.
"""

"""
=== Rewriting our pipeline one more time ===

Before we continue, let's rewrite our pipeline one last time as a function
(I will explain why in a moment -- this is so we can easily measure its performance).

"""

# Rewriting our pipeline one last time, as a single function
def pipeline(input_file, output_file):
    # 1. Input stage
    df = get_life_expectancy_data(input_file)

    # 2. Processing stage
    stats_summary = LifeExpectancyData()
    stats_summary.load_statistics(df)

    # 3. Output stage
    stats_summary.save_to_file(output_file)

"""
=== Performance ===

In the second stage, we said that one thing that could
go wrong was performance bugs.
How do we measure performance?

Three key performance metrics:

- Throughput

    What is throughput?
    How fast the pipeline runs, measured per input row or input item.

    Running time almost always varies depending on the size of the input
    dataset!
    Often linear: the more input items, the longer it will take to run
    So it's useful to think about the time per input item.

    Throughput is the inverse of this:
    Definition / formula:
        (Number of input items) / (Total running time).

Let's take our pipeline and measure the total running time & the throughput.
"""

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
=== Additional exercises (skip depending on time) ===
"""

"""
Problem: input data could be missing
"""

# Exercise 7: Insert a row with a missing value. What happens?

# Solutions?

"""
Problem: input data could be private
"""

# Exercise 8: Insert private data into the CSV file. What happens?

# Solutions?

"""
Problem: software bugs
"""

# Exercise 9: Introduce a software bug

# Solutions?

"""
Problem: performance bugs
"""

# Exercise 10: Introduce a performance bug

# Solutions?

"""
Problem: order-dependent and non-deterministic behavior
"""

# Exercise 11: Introduce order-dependent behavior into the pipeline

# Exercise 12: Introduce non-deterministic behavior into the pipeline

# Solutions?

"""
Problem: output errors and exceptions
"""

# Exercise 13: Save the output to a file that already exists. What happens?

# Exercise 14: Call the program from a different working directory (CWD)
# (Note: CWD)

# Exercise 15: Save the output to a file that is read-only. What happens?

# Exercise 16: Save the output to a file outside the current directory. What happens?

# (other issues: symlinks, read permissions, busy/conflicting writes, etc.)

# Solutions?

"""
Problem: output formatting

Applications must agree on a common format for data exchange.
"""

# Exercise 17: save data to a CSV file with a wrong delimiter

# Exercise 18: save data to a CSV file without escaping commas

# Solutions?

"""
Problem: readability and usability concerns --
    too much information, too little information, unhelpful information
"""

# Exercise 19: Provide too much information as output

# Exercise 20: Provide too little information as output

# Exercise 21: Provide unhelpful information as output

# Solutions?



"""
=== Advantages of software view ===

Advantages of thinking of data processing pipelines as software:

- Software *design* matters: structuring code into modules, classes, functions
- Software can be *tested*: validating functions, validating inputs, unit & integration tests
- Software can be *reused* and maintained (not just a one-off script)
- Software can be developed collaboratively (Git, GitHub)
- Software can be optimized for performance (parallelism, distributed computing, etc.)

It is a little more work to structure our code this way!
But it helps ensure that our work is reusable and integrates well with other teams, projects, etc.

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

From Edsgar Dijkstra:

    "Elegance is not a dispensable luxury but a factor that decides between success and failure."

The fundamental abstraction we will use in this course is...
the dataflow graph!

A dataflow graph is an abstraction (why?), but it is a very useful one.
It will help put all problems about data processing into context and help us understand how
to develop, understand, profile, and maintain data processing jobs.

It will provide a common framework for the rest of the course.
"""

# What a main function is: the default thing that you run when
# running a program.
# Sometimes called an "entrypoint"
# __name__: a variable that stores the name of the module being run

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

# Test file: main_test.py

# What have we found? If importing lecture.py as
# a library, the main function (above) doesn't get run.
# If running it directly from the terminal,
# the main function does get run.
