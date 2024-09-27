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

# Load the data from life-expectancy.csv into a pandas DataFrame
# Pandas documentation:
# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
import pandas as pd
df = pd.read_csv("life-expectancy.csv")

# Print the first 5 rows of the DataFrame
print("Hello")
print(df.head())

"""
Step 2: Do some processing
"""

# Print keys
print(df.keys())

min_year = df["Year"].min()
max_year = df["Year"].max()

print("Minimum year: ", min_year)
print("Maximum year: ", max_year)

avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()

print("Average life expectancy: ", avg)

# 3. Save the output
out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
out.to_csv("output.csv", index=False)

# (Side note on gitignore)

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

"""

"""
Design constraints

What are some design constraints or limiting factors that data processing pipelines might have to deal with?

1.
2.
3.
4.

=== Overview of course schedule ===

Overview of the schedule (tentative), posted at:
https://github.com/DavisPL-Teaching/119/blob/main/schedule.md

"""

"""
=== Closing with a quote from Patrice Koehl ===

From [Patrice Koehl](https://www.cs.ucdavis.edu/~koehl/):

    "
        Where is the wisdom we have lost in knowledge?
        Where is the knowledge we have lost in information?
        Where is the information we have lost in data?
    "

    With apologies to T.S. Eliot.
"""
