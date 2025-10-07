
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
=== Poll ===

1. Which stage do you think is likely to be the most computationally intensive part of a data processing pipeline?

2. Which stage do you think is likely to present the biggest opportunity for failure cases, including crashes, ethical concerns or bias, or unexpected/wrong/faulty data?

===============================================================
"""

"""
=== Rewriting our pipeline one more time ===

Before we continue, let's rewrite our pipeline one last time as a function
(I will explain why in a moment -- this is so we can easily measure its performance).
"""

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
