"""
Friday, October 3

Part 3:
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

# # A simple example:
# min_year = df["Year"].min()
# max_year = df["Year"].max()
# print("Minimum year: ", min_year)
# print("Maximum year: ", max_year)
# avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
# print("Average life expectancy: ", avg)

# # Tangent:
# # We can do all of the above with df.describe()

# # Save the output
# out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
# out.to_csv("output.csv", index=False)

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
"""
