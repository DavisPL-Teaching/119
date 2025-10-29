"""
October 10

Part 6:
Recap on Throughput & Latency and Conclusion

Recap from last time:

Throughput:
    Measured in number items processed / second

    N = number of input items (size of input dataset(s))
    T = running time of your full pipeline
    Formula =
        N / T

Latency:
    Measured for a specific input item and specific output

    Formula =
        (time output is produced) - (time input is received)

    Often (but not always) measured for a pipeline with just
    one input item.

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
# f()

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

# NB: If importing lecture.py as
# a library, the main function (above) doesn't get run.
# If running it directly from the terminal,
# the main function does get run.
# See test file: main_test.py
