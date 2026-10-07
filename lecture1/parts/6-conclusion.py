"""
October 7

Part 6:
Recap on Throughput & Latency and Conclusion

Throughput:
    Measured in number items or rows processed / second

    N = number of input items or rows (size of input dataset(s))
    T = running time of your full pipeline
    Formula =
        N / T

Latency:
    Measured for a specific input item and specific output

    Formula =
        (time output is produced) - (time input is received)

    Often (but not always) measured for a pipeline with just
    one input item.

    --> note on your HW! because you will need to take the input dataset(s)
        for part 1, and define a version of each dataset with only one input row.

=== Poll ===

A health company's servers process 12,000 medical records per day.
The medical records come in at a uniform rate between 9am and 9pm every day (1,000 records per hour).
The company's servers submit the records to a back-end service that collects them throughout the hour, and then
processes them at the end of each hour to update a central database.

What is the throughput of the pipeline?

What number would best describe the *average latency* of the pipeline?
Describe the justification for your answer.

https://forms.gle/3U3LspuTUbpAFY5Z8

1.:
    12,000 / day
    16.66 / minute
        ===> 1,000 / hour

    Throughput = N / T
    N = 12,000 items
    T = 9am to 9pm = 12 hours
    12,000 / 12 hours = 1,000 / hr
    days: 12,000 / 0.5 day = ...

    Latency:

        Medical records come in at a uniform rate
        Worst case scenario: medical record comes at the beginning of the hour:
            takes 60 minutes to process
        Best case scenario: medical record comes at the end of the hour:
            immediately processed

        Average: roughly 30 minutes on average.

    Main points:
        - Apply formulas
        - Latency you want to be thinking at an individual item / record / row level

    Correct answers:
        1000 items/hr or 16.67 / minute
        30 minutes
"""

"""
...

Let's see an example

We need a pipeline so that we can measure the total running time & the throughput.

This example pipeline uses the country dataset

see throughput_latency.py
"""

import pandas as pd

def get_life_expectancy_data(filename):
    return pd.read_csv(filename)

# Wrap up our pipeline - as a single function!
# You will do a similar thing on the HW to measure performance.
def pipeline(input_file, output_file):
    df = get_life_expectancy_data(input_file)
    min_year = df["Year"].min()
    max_year = df["Year"].max()
    # (Commented out the print statements)
    # print("Minimum year: ", min_year)
    # print("Maximum year: ", max_year)
    avg = df["Period life expectancy at birth - Sex: all - Age: 0"].mean()
    # print("Average life expectancy: ", avg)
    # Save the output
    out = pd.DataFrame({"Min year": [min_year], "Max year": [max_year], "Average life expectancy": [avg]})
    out.to_csv(output_file, index=False)

# SEE throughput_latency.py.

# import timeit

def f():
    pipeline("life-expectancy.csv", "output.csv")

# Run the pipeline
f()

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
=== Memory usage (also skip :) ) ===

What about the equivalent of memory usage?

I will not discuss this in detail at this point, but will offer a few important ideas:

- Input size:
    "memory required by a pipeline" is
    roughly proportional to size of all input datasets
        (That's the same as that parameter N that we saw earlier)

- Output size:
    "memory required by a pipeline" is
    also related to size of all output datasets

- Window size:
    For example: in the healthcare poll for today, window size could be defined
    as "how many records are being processed at any given moment, in the worst case"

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

From a previous year, not updated for this year

Check out the file structure in the GitHub repository for a complete
list of topics.

=== Closing thoughts ===

We defined a dataflow graph, which we argued is a model of computation for general
data processing programs

    A better model of what data processing software is than a traditional program

We saw (and will see) that using dataflow graphs can be helpful to think about properties
of our pipeline, such as ordering/dependence, data validation, performance.

Throughput&latency can be roughly calculated from the dataflow graph
    (We'll talk about how to do that)

Quote:

    "Every problem in software engineering can be solved by another layer of abstraction."
    https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering

A dataflow graph is an abstraction (why?), but it is a very useful one.
It will help put all problems about data processing into context and help us understand how
to develop, understand, profile, and maintain data processing jobs.

It's a good human-level way to understand pipelines, and
it will provide a common framework for the rest of the course.
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
