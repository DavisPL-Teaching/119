# Lecture 2: The Shell

## Oct 7 (Monday)

Announcements:

- HW0 and participation grades posted

- You can receive partial credit for submitting HW0 late.
  HW0 is used to associate your email with your name/ID, so you
  will need to submit HW0 before seeing any of your participation scores.

- Questions?

Plan for today:

- Poll

- Cleaned up example from last time: Throughput & Latency

- Start lecture 2

  + Lecture 2 will focus on the shell (your terminal)

Looking forward:
return to data processing in Pandas starting from Lecture 3
(input validation, cleaning, data wrangling, transformations, scraping, etc.)
parallel/distributed data processing as soon as possible but likely
not until halfway through the quarter.

### Following along

`git status`, `git stash`, and then `git pull`
`cd lecture2` -- the same `python3 -i lecture.py`

### Poll

What are the units of throughput?

https://forms.gle/HkpcNKrT9QnxTi269
https://tinyurl.com/mesbhpdk

Finishing some definitions:

- Throughput = Amount of data (or number of input items)
  processed per unit time

- Latency = Amount of time to process a single data item

For a cleaned up example, see lecture1/throughput_latency.py.

These concepts and terminology are fundamental in computer networking.
For example, you may have seen wifi network advertised in terms of
throughput or bandwidth in Mbps:
https://www.speedtest.net/

We will come back to this later on!
For now: the fundamental performance characteristics of ANY data processing
pipeline can be summarized by throughput and latency.

## Oct 9 (Wednesday)

Announcements:

- Add deadline is tomorrow (Oct 10) (Drop deadline: Oct 22)

- Midterm currently scheduled in-class for Nov 1 (tentative)

Plan:

- Start with the poll

- Shell: looking around, navigating, getting help, command arguments, I/O, Dangers of the shell

- Recap & Q+A

- (Next time) Git & GitHub basics

### Following along

git status, git stash, git pull

### Poll

Continuing from last time's poll:
Which of the following are valid units of latency?

https://forms.gle/asAcaEewqAvk4PvB8
https://tinyurl.com/2668rc6c

## Oct 11 (Friday)

Announcements:

- HW1 is in the works (planned release on Monday)

Plan:

- Start with the poll

- Continue lecture on the shell

  + "Getting help" (continued)

  + "Doing things"

  + Command arguments

  + I/O

  + Understanding git

  + Dangers of the shell

If you haven't yet:
do a git status, git stash, git pull.

### Poll

Which of the following are "informational" commands?
Informational commands are like "looking around"; they do not change the underlying state of the shell.

https://forms.gle/vMdYx59n1vqFEbtb6
https://tinyurl.com/58nsj63c
