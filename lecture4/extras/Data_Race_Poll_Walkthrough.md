Clarifying questions:

    x += 1
    ^^^^^ read followed by a write!
    x = x + 1

think of it as 2 statements:

    temp = read from x
    write temp + 1 into x

    ^^^
    temp = x
    x = temp + 1

    Simpler example:

        worker 1:            worker 2:
        x += 1               x += 1

        read(x)              read(x)
        write(x + 1)         write(x + 1)

    values you can end: 1, or 2

    How to get 1?

    worker1: read 0
    worker2: read 0
    worker1: write 0 + 1 = 1
    worker2: write 0 + 1 = 1

    end result: 1

Can we get the value 200?
A: Yes, if for example worker1 increments 100 times, then worker 2 increments 100 time (no interleaving)

Can we get the value 100?

Yes:
Idea: worker1 finishes, worker2 hasn't finished yet:
worker1: 0 -> 1, 1 -> 2, ..., 99 -> 100

worker2: 0 ->                           -> 1, 1 -> 2, 2 -> 3,
    ..., 99 -> 100.

Can we get 120?

worker2 reads x when it's at the value 20 instead of 0.
worker1: 0 -> 1, 1 -> 2, ..., 99 -> 100

worker2:                 20             -> 21 -> ... -> 100.

0 to 5 instead of 0 to 100:
worker1: 0 -> 1, 1 -> 2,      2 -> 3, 3 -> 4, 4 -> 5
worker2:                 2 ->                        3, 3 -> 4, 4 -> 5, 5 -> 6, 6 -> 7.

Final boss: Can we get a value between 0 and 100? Like 70?

We should try to construct an execution where both worker1 and worker2
overwrite all of each other's work!

worker1: 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 4,       1                              -> 2
worker2: 0                               -> 1, 1 -> 2, 2 -> 3, 3 -> 4, 4 -> 5

We got 2! with two workers, 0 to 5.

We can generalize this to two workers to get 2 (or any value between 2 and 100)
with 100 increments.

Probably not a way to get 0 or 1.

**Correct answer should be: any value between 2 and 200.**

Very scary!

A simple program with a data race turned out to be extremely counterintuitive
to think about.

    - I won't ask about an example this complex on the midterm, but I might
      ask about something simpler like

        worker1                  worker2
        x += 1                    x += 1
        x += 1

Concurrent programming is very hard! It's better if we can write code in a way
that *exposes* parallelism but not concurrency - tasks that are parallel run in parallel,
and we don't have to worry about concurrency and data races.
