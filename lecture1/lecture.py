"""
Lecture 1: Introduction to data processing pipelines

=== Poll ===

Today's poll is to help me understand your background in Python and command line/Git.
(I will also ask about your background in HW0.)

https://forms.gle/h53wSrkeaM4R28Gu9
https://tinyurl.com/ypevcu9u

=== Following along ===

Try this!

1. You will need to have Git installed (typically installed with Xcode on Mac, or with Git for Windows). Follow the guide here:

    https://www.atlassian.com/git/tutorials/install-git

    Feel free to work on this as I am talking and to get help from your neighbors.
    I can help with any issues after class.

2. You will also need to create an account on GitHub and log in.

3. Go to: https://github.com/DavisPL-Teaching/119

4. If that's all set up, then click the green "Code" button, click "SSH", and click to copy the command:

    git@github.com:DavisPL-Teaching/119.git

5. Open a terminal and type:

    git clone git@github.com:DavisPL-Teaching/119.git

6. Type `ls`.

    You should see a new folder called "119" in your home folder. This contains the lecture notes and source files for the class.

7. Type `cd `119/lecture1`, then type `ls`.
   Lastly type `python3 lecture.py`. You should see the message below.
"""

print("Hello, ECS 119!")

"""
If some step above didn't work, you may be missing some of the software we
need installed. Please complete HW0 first and then let us know if you
are still having issues.

=== The basics ===

I will introduce the class through a basic overview, or "toy model"
of what a data procesisng pipeline is. Throughout, we will also see
some of the constraints that data processing pipelines have to satisfy,
how they interact with one another, and so on.
This will lead to an overview of topics covered in the class.

Recall "discussion scenarios" from the previous lecture.

EXAMPLE 1:
I have a spreadsheet containing 1000 movies I have seen or want to see,
dates watched, and movie ratings.
I built a Python application which loads the spreadsheet,
filters out movies based on a recently viewed or highest-rated sorting,
and allows me to mark a movie as seen or to edit any movie ratings.
It also collects statistics about all the movies.
All of this data is then saved back to the spreadsheet.

EXAMPLE 2:
I have written a website scraper that reads data from Wikipedia.
I re-run the scraper every week to get the latest data.
It opens up all Wikipedia sites that correspond to cities in the world,
extracts the population of each city, the area, and the country it is located
in. Once all of this data is collected, it stores it in a structured
format and saves it to a database, then queries the database for the
top 100 most population-dense cities and outputs these to a file
biggest_cities.txt.

What do these scenarios have in common?
Suggestions:
- Write the data to CSV
- ...

3 stages -- related to something called the "Extract, Transform, Load" model (ETL)

What are the components of a data processing pipeline?

0. Description of the task that you want to complete.
1. Input source -- get your input from somewhere
2. Processing stage -- do some transformations on your data,
    add additional data fields, modify fields, calculate summary
    statistics, etc.
3. Output -- save the results to a file or a database; display
    them to the user; etc.
"""

"""
Step 1: Getting a data source

Useful sites:
- https://ourworldindata.org/data
- sklearn
"""

# # Load the data from life-expectancy.csv into a pandas DataFrame
# # Pandas documentation:
# # https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# import pandas as pd
# df = pd.read_csv("life-expectancy.csv")

# # Print the first 5 rows of the DataFrame
# print("Hello")
# print(df.head())

"""
Step 2: Do some processing
"""

# # Print keys
# print(df.keys())

# min_year = df["Year"].min()
# max_year = df["Year"].max()

# print("Minimum year: ", min_year)
# print("Maximum year: ", max_year)

# avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()

# print("Average life expectancy: ", avg)

"""
Stage 3. Save the output
"""

# out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
# out.to_csv("output.csv", index=False)

# # (Side note on gitignore)

"""
Graphical view

We can view all of the above steps as something called
a directed acyclic graph (DAG).
What do I mean and how?

It's a flow chart of input sources,
processing stages (often called "operators"),
and outputs.

                       -> min ->
(life-expectancy.csv)  -> max ->  output.csv
                       -> avg ->

Why is this useful?

- We'll use this to think about parallelism
- We'll use this to think about performance.

=== Recap of what we covered today ===

- Any data processing pipeline can be thought of as having 3 stages:
    input source, processing, and output
- Data processing pipelines can be drawn as directed acyclic graphs (DAGs).

=======================================================================

=== Monday, September 30 ===

(See README.md for announcements and plan.)

=== Following along ===

Reminder to follow along:
https://github.com/DavisPL-Teaching/119

(I will go through the steps again in class)

Navigate to the directory you want:
- ls to show directories
- cd <directory> to move into the directory

If you already cloned the repo, then this time, you need to get any code updates.
Do the following:

- git status
- git stash
- git pull

=== A tangent on pacing ===

- The pacing might be a bit slow right now for some of you -- especially if you have prior experience
  with Python, pandas, Git, etc.
  (HW0 results so far: 100% have used Python, 80% Pandas, 75% Git)

- We do have varying levels of background including some who have not used some of these tools
  before. So please be patient with us for the first few lectures.

- 80% of you have only limited experience with command line in particular, so we will spend some additional
  time in Lecture 2 on software development tools.

- There will be a mid-quarter survey (around 4 weeks in) to see if we are going too slow or too fast
  and I will adjust things accordingly!

=== Poll ===

1. Which stage do you think is likely to be the most computationally intensive part of a data processing pipeline?

2. Which ostage do you think is likely to present the biggest opportunity for failure cases, including crashes, ethical concerns or bias, or unexpected/wrong/faulty data?

https://forms.gle/Kv39iq33KDjJy3ir6
https://tinyurl.com/3tthzry7

=== Data processing pipelines as software ===

Some of you may know about tools like Jupyter notebooks, Google Colab, or Excel.
(What is the most widely used data processing tool? Answer: Excel)

So why aren't we using those tools? :)

In this course, I want to encourage us to think about data processing pipelines as real software.
That means:
- Software *design* matters: structuring code into modules, classes, functions
- Software can be *tested*: validating functions, validating inputs, unit & integration tests
- Software can be *reused* and maintained (not just a one-off script)
- Software can be developed collaboratively (Git, GitHub)
- Software can be optimized for performance (parallelism, distributed computing, etc.)

It is a little more work to structure our code this way!
But it helps ensure that our work is reusable and integrates well with other teams, projects, etc.

Let's consider how to write the minimal data processing pipeline we saw last time
as a more structured software pipeline.

Useful tutorial on Pandas:
https://pandas.pydata.org/docs/user_guide/10min.html
https://pandas.pydata.org/docs/user_guide/indexing.html
"""

import pandas as pd

# Step 1: Getting a data source
# creating a DataFrame
# DataFrame is just a table: it has rows and columns, and importantly,
# each column has a type (all items in the column must share the same
# type, e.g., string, number, etc.)
# df = pd.read_csv("life-expectancy.csv")

def get_life_expectancy_data(filename):
    """
    This is called a docstring

    Take in CSV data from life-expectancy.csv
    Return a DataFrame of the data.
    """
    df = pd.read_csv(filename)
    return df

"""
Running the code

It can be useful to have open a Python shell while developing Python code.

There are two ways to run Python code from the command line:
- python3 lecture.py
- python3 -i lecture.py

Let's try both
"""

# Step 2: Do some processing
# min_year = df["Year"].min()
# max_year = df["Year"].max()
# print("Minimum year: ", min_year)
# print("Maximum year: ", max_year)
# avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
# print("Average life expectancy: ", avg)

class LifeExpectancyData:
    """
    Our data will include:
    - maximum year
    - minimum year
    - average of all the life expectancies
    """

    def __init__(self):
        """
        Initialize fields

        self keyword: refers to the object itself
        """
        self.min = None
        self.max = None
        self.avg = None

    def load_statistics(self, df):
        """
        Read in data from the DataFrame
        and store it in our clas
        """
        self.min = df["Year"].min()
        self.max = df["Year"].max()
        self.avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()

    def save_to_file(self, filename):
        out = pd.DataFrame({"Min year": [self.min], "Max year": [self.max], "Average life expectancy": [self.avg]})
        out.to_csv(filename, index=False)

    def get_from_user(self):
        # Instead of loading from a file, get the data via user input.
        raise NotImplementedError

# Tangent:
# We can do all of the above with df.describe()

# Step 3: save the output
# out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
# out.to_csv("output.csv", index=False)
# Do this above

"""
Let's revisit our criteria from before. How does this help?
"""

# - Software design

# Exercise 1: Revise the class above so that the input is taken from an argument, instead of
# provided as a hardcoded filename

# - Software testing

# Exercise 2: Validate the the input has the correct number of countries.
# (Q: What is the correct number? A: More on this in a bit)

# We can use pytest for testing
# conda list pytest
# conda install pytest
import pytest

# How pytest works:
# Any function with the prefix test_ is considered
# a test.
# We can run all tests with pytest lecture.py
# We can use @pytest.mark.skip decorator to skip
# tests -- nskip to run test
# @pytest.mark.skip
def test_get_life_expectancy_data():
    data = get_life_expectancy_data("life-expectancy.csv")
    countries = data["Entity"].unique()
    assert len(countries) == 261

# 261 countries!
# (This is a property of our dataset -- which countries
# get included or not is a geopolitical and ethical question)

# - Software reuse

# Exercise 3:
# Reuse the class to get input in a different way: from the user
# TODO try this exercise.

"""
Recap of what we covered today:

- Data processing pipelines as software

- Software design best practices, modularity, and reuse

- A little bit about data validation -- i.e. determining whether
  whatever assumptions we have about the data may actually be
  correct.

"""

# - Collaborative development
# Why is the above code better for collaborative development?

# - Performance optimization
#   (More on this shortly)

"""
=== Design constraints ===

Recall that we talkd on the first lecture about software components + design constraints.
Let's talk more about the design constraints bit.

What could go wrong in our toy pipeline above?
Let's go through each stage at a time:

1. Input stage

What could go wrong here?


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

"""

"""
Problem: input data could be malformed
"""

# Exercise 4: Insert a syntax error into the CSV file. What happens?

# Exercise 5: Insert a row with a value that is not a number. What happens?

# Solutions?

"""
Problem: input data could be wrong
"""

# Exercise 6: Delete a country or add a new country. What happens?

# Solutions?

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
2. Processing stage

What could go wrong here?
"""

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
Problem: order-depenent and non-deterministic behavior
"""

# Exercise 11: Introduce order-dependent behavior into the pipeline

# Exercise 12: Introduce non-deterministic behavior into the pipeline

# Solutions?

"""
3. Output stage

What could go wrong here?
"""

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
In the second stage, we said that one thing that could

One aspect of particular interest to us in this class is the performance in the second
stage. How do we measure performance?

=== Performance ===

Three key performance metrics:

- Throughput

- Latency

- Memory usage

Let's measure the performance of our toy pipeline.

Timeit:
https://docs.python.org/3/library/timeit.html

Example syntax:
timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
"""

import timeit

def measure_throughput():
    raise NotImplementedError

def measure_latency():
    raise NotImplementedError

def measure_memory_usage():
    raise NotImplementedError

"""
=== Overview of the rest of the course ===

Overview of the schedule (tentative), posted at:
https://github.com/DavisPL-Teaching/119/blob/main/schedule.md

=== Closing quotes ===

From Patrice Koehl:
https://www.cs.ucdavis.edu/~koehl/:

    "Where is the wisdom we have lost in knowledge?
    Where is the knowledge we have lost in information?
    Where is the information we have lost in data?"

    With apologies to T.S. Eliot.

Data processing is all about extracting wisdom from data.
But each of these steps can go wrong!

From Edsgar Dijkstra:

    "Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it. And to make matters worse: complexity sells better."

I'd like to encourage us to think about how to build pipelines that are as *simple* as possible
-- organized into careful components, with helpful abstractions -- rather than having
expanding components and needless complexity.

Why? Simpler pipelines are more reliable, easier to develop, easier to understand, and easier to maintain.

Tools are adopted not just because of what they can do, but because of how much they can do in the most
intuitive and direct way possible.

The tools we see in this class will help us achieve the right abstractions to achieve this simplicity.

"""
