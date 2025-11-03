"""
Lecture 4: Parallelism

Part 1: Motivation
(Oct 24)

=== Discussion Question and Poll ===

Which of the following is an accurate statement about Git's core philosophies?

https://forms.gle/zB1qhdrP2xXswHMX8

===== Introduction =====

So far, we know how to set up a basic working data processing pipeline
for our project:

- We have a prototype of the input, processing, and output stages
  and we can think about our pipeline as a dataflow graph (Lecture 1)

- We have used scripts and shell commands to download any necessary
  data, dependencies, and set up any other system configuration (Lecture 2)
  (running these automatically if needed, see HW1 part 3)

How did we build our pipeline?

So far (in Lecture 1 / HW1), we have been building our pipelines in Pandas

- Pandas can efficiently representing data in memory as a DataFrame

- Pandas uses vectorization - you studied this a little in HW1 part 2

The next thing we need to do is **scale** our application.

=== What is scaling? ===

Scalability is the ability of a system to handle an increasing amount of work.

=== Why scaling? ===

Basically we should scale if we want one of two things:

1. Running on **more** input data
    e.g.:
    + training your ML model on the entire internet instead of a dataset of
      Wikipedia pages you downloaded to a folder)
    + update our population pipeline to calculate some analytics by individual city,
      instead of just at the country or continent level

2. Running **more often** or on **more up-to-date** data
    e.g.:
    + re-running your pipeline once a day on the latest analytics;
    + re-running every hour to ensure the model or results stay fresh; or even
    + putting your application online as part of a live application
      that responds to input from users in real-time
      (more on this later in the quarter!)

Questions we might ask:

- How likely would it be that you want to scale for a toy project?
  For an industry project?

  A: probably more likely for an industry project.

- What advantages would scaling have on an ML training pipeline?

=== An example: GPT-4 ===

Some facts:
    + trained on roughly 13 trillion tokens
    + 25,000 A100 processors
    + span of 3 months
    + over $100M cost according to Sam Altman
    https://www.kdnuggets.com/2023/07/gpt4-details-leaked.html
    https://en.wikipedia.org/wiki/GPT-4

(And the next generation of models have taken even more)

Contrast:

    our population dataset in HW1 is roughly 60,000 lines and roughly 1.6 MB on disk.'

    Over 1 million times less data than the amount of tokens for GPT-4!

Conclusion: scaling matters.
NVIDIA stock:

    https://www.google.com/finance/quote/NVDA:NASDAQ?window=5Y

=== Thinking about scalability ===

Points:

- We can think of scaling in terms of throughput and latency

    See extras/scaling-example.png for an example!

    If your application is scaling successfully,
    double the # of workers or processors => double the throughput
    (best case scenario)

    double the # of processors => half the latency? (Y or N)

        A: Not necessarily

        Often latency is not affected in the same way.

If we can scale our application successfully,
we are typically looking to increase the throughput of the application.

=== A note about Pandas ===

Disdavantage of Pandas: does not scale!

- Wes McKinney, the creator of Pandas:
    "my rule of thumb for pandas is that you should have 5 to 10 times as much RAM as the size of your dataset"

    https://wesmckinney.com/blog/apache-arrow-pandas-internals/

Exercise:

    Check how much RAM your personal laptop has.
    According to McKinney's estimate, how much how large of a dataset in population.csv
    could your laptop handle?

(Let me show how to do this)

My answer: 18 GB

Next time at the start of class, we'll poll the class for various
answers and figure out how large of a dataset we could handle in Pandas.

Recap:

- We went over midterm topics
- We saw some motivation for why you might want to scale your application
- We defined scalability and types of scalability (running on more data vs. running more often)
- Pandas does not scale in this sense.

----- Where we ended for today -----

(Finishing up)

Recall: statement from Wes McKinney

Uncomment and run this code to find out your RAM
"""

import subprocess
import platform

def get_ram_1():
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["sysctl", "-nh", "hw.memsize"])
    elif system == "Linux":
        subprocess.run(["grep", "MemTotal", "/proc/meminfo"])
    elif system == "Windows":
        print("Windows unsupported, try running in WSL?")
    else:
        print(f"Unsupported platform: {system}")

# Run the above
print("Amount of RAM on this machine (method 1):")
get_ram_1()

import psutil
def get_ram_2():
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)
    print(f"{ram_gb:.2f} GB")

print("Amount of RAM on this machine (method 2):")
get_ram_2()

"""
Poll:

Answers:

Method 1:
    8.5, 8.6, 17.1, 15, 17.1, 16.5, 17.1

Method 2:
    8, 8, 16, 7.62, 15.61, 14.45, 15.4, 7.82, 16, 15.3, 31.6
"""

method1 = [8.5, 8.6, 17.1, 15, 17.1, 16.5, 17.1]
method2 = [8, 8, 16, 7.62, 15.61, 14.45, 15.4, 7.82, 16, 15.3, 31.6]

average1 = sum(method1) / len(method1)
average2 = sum(method2) / len(method2)

print(f"method 1 avg: {average1}", f"method 2 avg: {average2}")

ram_needed = average2 / 10

print(f"Using method 2: we can handle a dataset up to size: {ram_needed} GB")

"""
Please fill out your answers in the poll:

https://forms.gle/sqGrHBdQBrykDoSdA

Roughly, we can process like _____ as much data
and then we'll a bottleneck.

population.csv from HW1: 1.5 MB

According to the class average, we could go up to 1000x the population
and still handle it with Pandas, beyond that we will run out of space,
according to McKinney's statement.
"""
