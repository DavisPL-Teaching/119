# In-class poll answers

Sep 24:
Tools required and characteristics and needs of your application will change drastically with the size of the dataset.

Sep 26:
N/A

Sep 29:
1) One possible answer: input file does not exist
2) No, because the maximum row of a dataset is not always unique.

Oct 3:
All except B ("Will speed up the development of a one-off script")

Oct 6:
1) Edges from:
read -> max, min, and avg
max, min, and avg -> print
max, min, and avg -> save

2) read -> print or read -> save (give a specific example)

Oct 8:
True, False, False.

Oct 10:
1) Throughput = 1,000 records/hour assuming the full pipeline is measured from 9am to 9pm.
2) 30 minutes on average
3) From the perspective of the patient (individual row level): uniformly distributed between 0min and 60min delay.

Oct 13:
1) hrs, ms, s, ns
2) F F F T T F

Oct 15:
Correct answers: 1, 2, 3, 4, 5, and 7 (all except 6: "To load & use pandas to calculate the max and average of a DataFrame")

Oct 17:
1) B, C, and D
2) B, C, D, E, and F (all except "A: A python3 'Hello, world!' program works only on certain operating systems")

Oct 20:
ls, ls -alh, echo $PATH, python3 --version, conda list, git status, cat, less

Oct 22:
1) Some possible answers: `cd folder/`, `cp file1.txt file2.txt`
2) Some possible answers: `ls -alh`, `python3 --version`

Oct 24:
B, E, and F.

Oct 27:
1, 2: no one correct answer, most answers were clustered 8 GB or 16GB
3: Pandas requires 5-10x the amount of RAM as your dataset, so for 16GB you should have gotten 1.6GB to 3.2GB for the lagest dataset you can handle.

Oct 29:
1. Parallel
2. Parallel + Concurrent
3. Parallel + Concurrent
4. Concurrent + Distributed
5. Parallel + Distributed
6. Parallel + Concurrent + Distributed

Oct 31:
1. Intended answer was between 0 and 200;
to be fully precise, the correct answer should be any value between 2 and 200 (inclusive).

2. ABDEFG
   Concurrency, Parallelism, Contention, Race Condition, Data Race -
   and Spooky Halloween Vibes, because data races are scary!! :-)

Nov 3:
Data parallelism (at tasks 1 and 2)
No task parallelism
Pipeline parallelism from 1 -> 2 and 2 -> 3.
(Pipeline parallelism will not appear on midterm)

Nov 7:
1. Data parallelism: **single node**
Task parallelism: **between a pair of nodes**
Pipeline parallelism: **between a pair of nodes**

2. Answer is yes. For instance, splitting one node "task" into two separate tasks could reveal additional pipeine and task parallelism that would not be present in the graph.

Nov 10:
T = 300 ms
S = 3 ms
Speedup <= T / S = 100x.
Maximum speedup is 100x (same as the # of data items - this is not a coincidence).

Nov 12:
C and E: CPU cores & RAM available

Nov 14:
5, 6, and 8.
Note that, depending on assumptions about how regular the timestamps are or if the input data is sorted by row #, it may be possible to make these data-parallel also.
It is just not quite as straightforward as the others.

Nov 17:
1: Lazy, 2: Lazy, 3: Not Lazy
Bonus: 5ms + 5ms + 5ms = 15 ms.

Nov 19:
Multiple solutions are possible
Map stage should describe a map on each input row (T1) to an output row (T2)
Reduce stage should describe how to combine two output rows (two T2s, get a single T2)
Example solution:
Map stage: map each row to (city name, avg_temp / population)
Reduce stage: for (city1, ratio1), (city2, ratio2), return (city3, ratio3) where ratio3 = max(ratio1, ratio2) and city3 is the corresponding city.

Nov 21:
Narrow: 1, 4, 5, 7
Wide: 2, 3, 6
