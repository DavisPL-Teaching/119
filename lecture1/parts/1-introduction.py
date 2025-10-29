"""
Lecture 1: Introduction to data processing pipelines

Part 1: Introduction

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
"""
