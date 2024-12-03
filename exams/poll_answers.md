# In-class poll answers

Sep 25: N/A

Sep 27: N/A

Sep 30: (1) processing stage (2) typically the input stage

Oct 2: options 1, 2, 5, 6, 7 (everything except "To take advantage of pandas", "To run and debug code interactively", and "To make a one-off script easier to write")

Oct 4: (1) all 5 options (2) subjective (no correct answer), common answers include 193, 195, 197 (and many others).

Oct 7: "Data items per second", "Bytes per second", and "Rows per second"

Oct 9: "Seconds" and "Milliseconds"

Oct 11: the first 7 options (up to conda list pandas) + git status

Oct 14: (1) add, commit, push (2) options 1, 2, 3

Oct 16: options 2, 5 only

Oct 18: the last 2 options (a question of this form will not appear on the exam)

Oct 21: (1) 1, 2 only (2) 1, 5 only

Oct 23: (1) Parallel (2) Parallel + Concurrent (3) Parallel + Concurrent (4) Concurrent + Distributed (5) Parallel + Distributed (6) Parallel + Concurrent + Distributed

Oct 25: (1) Any integer is possible (note that I am encouraging you to adopt the "simplified view" here that does not worry about the underlying architecture: you may assume that if a read/write occurs at the same memory location at the same time, the data gets corrupted and can be any value). (2) Concurrency, Parallelism, Contention, Race Condition, and Data Race.

Oct 30: Data parallelism and pipeline parallelism

Nov 1: (1) 300 / 3 = 100x (2) 400 / 3 = 133.33...x

Nov 4: Task: first+second or Map+second. Pipeline: first+Map, Map+Semijoin, second+Semijoin, Semijoin+Map, or Map+Distinct. Data: all nodes are valid answers. In practice, Distinct (presumably meaning to return all distinct input items) is the least parallelizable of these, the rest exhibit very clear data parallelism.

Nov 6: 3 (CPU cores) and 5 (memory/storage)

Nov 13: N/A

Nov 15: Vertical + Horizontal scaling, data parallelism, distribution, and should behave
   as if it were a normal collection type

Nov 18: 1, 2 lazy, 3 not lazy
Bonus: 5 + 5 + 5 = 15 ms.

Nov 20:
1. Narrow
2. Wide
3. Wide
4. Narrow
5. Narrow
6. Wide
7. Narrow

Nov 22:
Map: For each city, compute (city name, temp / population)
Reduce: Combine (name1, ratio1) + (name2, ratio2) by computing the maximum ratio between
   the two, and the city name which equals that maximum.
   (max_city, maximum(ratio1, ratio2).

Nov 25: 3 (not optimized for latency) and 8 (nondeterminism)

Nov 27: 2, 4, 5, 6.

Dec 2: 2ms; Yes, the latency would be higher

Dec 4:

Dec 6:
