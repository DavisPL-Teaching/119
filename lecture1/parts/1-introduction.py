"""
Lecture 1: Introduction to data processing pipelines

Part 1: Introduction

This lecture will provide a basic conceptual framework for the rest of the course.

Please bear with us if you have already seen some of this material before!
I will use the polls to get a sense of your prior background and adjust the pacing accordingly.

=== Tour of Git repository ===

This is the class Git repository.
This file is 119/lecture1/parts/1-introduction.py.

**Note on materials from prior iteration of the course:**
The GitHub repository contains some lecture notes from a prior iteration of the course.
You are welcome to look ahead in the notes, but please note that most content will change as I revise each lecture.
I will generally post the revised lecture before and after each class period.

=== Poll ===

Today's poll is to help me understand the overall class background including Python, command line and Git.
(I will ask about your background in more detail on HW0.)

https://forms.gle/mJWA56sVZ3T93j6S6

^^ To find this link: go to the lecture notes on GitHub:

Piazza -> pinned post of important links -> GitHub -> lecture1 -> lecture.py
https://piazza.com/

=== Poll results ===

(Go over the poll results)

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

7. Type `cd `119/lecture1/parts`, then type `ls`.

8. Lastly type `python3 1-introduction.py`. You should see the message below.
"""

print("Hello, ECS 119!")

"""
Let's see if that worked!

If some step above didn't work, raise your hand and I'll come around to try to help.

You may be missing some of the software we need installed.
If that's the case, I'll recommend that you complete HW0 first and hopefully
that will resolve the issue.

=== Short digression ===

- **Why use the command line?**

  Short answer: it's an important skill!

  Long answer:
  The command line is a primary way how engineers and AI agents interface with
  computers: installing software, running commands, etc. It's the
  "master switch" to get administrative access to anything that you want to do
  on any device.

  I do require learning how to use the command line for this course.
  Lecture 2 will provide an introduction to how to think about the command line.

  - Why not just use GUI tools?

  GUI tools only work if someone else already wrote them (they used the command line to write the tool).
  GUI tools are typically not available for server machines, cloud/Amazon compute, etc.

  You'll find that it is SUPER helpful to know the basics of the command line for stuff like installing software, managing dependencies, and debugging why installation didn't work.

  - Why not use AI to write commands?

  AI or Google can help you if you forget some syntax --
  I want you to understand how commands are running "under the hood" --
  it's an important skill for data engineering in practice.

=== The basics ===

I will introduce the class through a basic model of what a data processing
pipeline is, that we will use throughout the class.

We will also explore:
- Constraints that data processing pipelines have to satisfy
- How they interact with one another
- How to think about executing them - sneak peak of some future topics covered in the class.

To answer these questions, we need a basic model of "data processing pipeline" - Dataflow Graphs.

=== Starting point ===

Example scenario:

EXAMPLE:
You have compiled a spreadsheet of website traffic data for various popular websites (Google, Instagram, chatGPT, Reddit, Wikipedia, etc.). You have a dataset of user sessions, each together with time spent, login sessions, and click-through rates. You want to put together an app which identifies trends in website popularity, duration of user visits, and popular website categories over time.

This is a data processing job!

We need a *pipeline* (some code) to run the job.

What are the main "abstract" components of the data processing job in this scenario?

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

- A dataset
- Processing steps
- Some kind of user-facing output

closely related:
"Extract, Transform, Load" model (ETL)

What is an ETL job?

- **Extract:** Load in some data from an input source
    (e.g., CSV file, spreadsheet, a database)

- **Transform:** Do some processing on the data

- **Load:** (Sometimes a confusing name)
  we save the output to an output source.
    (e.g. CSV file, spreadsheet, a database)

"""

data = {
    "User": ["Alice", "Alice", "Charlie"],
    "Website": ["Google", "Reddit", "Wikipedia"],
    "Time spent (seconds)": [120, 300, 240],
}

# As dataframe:
# import pandas as pd
# df = pd.DataFrame(data)

# print(data)
# print(df)

"""
=== Question ===

Which of the above might be consider Extract, Transform, and Load?

======

So far, we got set up with a basic data processing pipeline (in Python)
and we introduced a conceptual model to think about these pipelines.

We'll continue this example in the next part.

"""
