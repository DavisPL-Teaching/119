"""
Lecture 1: Introduction to data processing pipelines

Part 1: The basics, following along, and "Hello, world" example.

This lecture will provide a basic conceptual framework for the rest of the course.

Please bear with us if you have already seen some material before!
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

5. Open a terminal (Command+Space terminal on mac) and type:

    git clone git@github.com:DavisPL-Teaching/119.git

6. Type `ls`.

    You should see a new folder called "119" in your home folder. This contains the lecture notes and source files for the class.

7. Type `cd 119/lecture1/parts`, then type `ls`.

8. Lastly type `python3 1-introduction.py`. You should see the message below.
"""

print("Hello, ECS 119!")

"""
Let's see if that worked!

If some step above didn't work, raise your hand and I'll come around to try to help.

You may be missing some of the software we need installed.
If that's the case, I'll recommend that you complete HW0 first and hopefully
that will resolve the issue.

***** Where we stopped for Sep 25 *****
"""

"""
=== REMINDER: FOLLOWING ALONG ===

https://github.com/DavisPL-Teaching/119

- Open terminal (Cmd+Space Terminal on Mac)

- `git clone <paste repository link>`

    + if you have already cloned, do a `git stash` or `git reset .`

- `git pull`

=== Starting point ===

Let's start with a basic example of some data processing code:

Example scenario:

EXAMPLE:
You have compiled a spreadsheet of website traffic data for various popular websites (Google, Instagram, chatGPT, Reddit, Wikipedia, etc.). You have a dataset of user sessions, each together with time spent, login sessions, and click-through rates. You want to put together an app which identifies trends in website popularity, duration of user visits, and popular website categories over time.

This is a data processing job!

We need a *pipeline* (some code) to run the job.
"""

data = {
    "User": ["Alice", "Alice", "Charlie"],
    "Website": ["Google", "Reddit", "Wikipedia"],
    "Time spent (seconds)": [120, 300, 240],
}

# Uncomment to run
# As dataframe:
# import pandas as pd
# df = pd.DataFrame(data)

# print(data)
# print(df)


"""
Running the code

It can be useful to have open a Python shell while developing Python code.

There are at least two ways to run Python code from the command line:
- python3 lecture.py
- python3 -i lecture.py

Let's try both.

=== Short digression ===

- **Why use the command line?**

  (More on this in Lecture 2)

  The command line is a primary way how engineers (and AI agents) interface with
  computers: installing software, running commands, etc. It's the
  "master switch" to get administrative access to anything that you want to do
  on any device.

  I do require learning how to use the command line for this course,
  which we will do in a bit more detail for Lecture 2.

  - Why not just use GUI tools?

  GUI tools only work if someone else already wrote them (they used the command line to write the tool).
  GUI tools are often not available for server machines, cloud/Amazon compute, etc.

  You'll find that it is SUPER helpful to know the basics of the command line for stuff like installing software, managing dependencies, and debugging why installation didn't work.

  - Why not use AI to write commands?

  Sure! AI or Google can help you if you forget some syntax.
  I want you to understand how commands are running "under the hood" --
  it's an important skill for data engineering in practice.

=== Recap ===

So far, we have a basic example of a data pipeline running.
We will build on this example to introduce important concepts for the rest of the class
(see `parts/` on the left-hand side in your code editor or file browser to see some of the topics
we are considering next).

We will also explore:
- Constraints that data processing pipelines have to satisfy
- How they interact with one another
- How to think about executing them, how to execute them *faster* - which ties in to
  future topics covered later in the class.

To answer these questions, we need a *model* of what a "data processing pipeline" is!
We will start from the simplest model, Extract-Transform-Load (ETL).
"""
