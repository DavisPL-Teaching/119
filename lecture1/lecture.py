"""
Lecture 1: Introduction to data processing pipelines

=== Poll ===

Today's poll is to help me understand your background in Python and command line/Git.
(I will also ask about your background in HW0.)

https://forms.gle/h53wSrkeaM4R28Gu9
https://tinyurl.com/ypevcu9u

=== Following along ===

Try this!

1. Go to: https://github.com/DavisPL-Teaching/119

2. You will need to create an account on GitHub and log in.

3. You will need to have Git installed (typically installed with Xcode on Mac, or with Git for Windows). Follow the guide here:

    https://www.atlassian.com/git/tutorials/install-git

    Feel free to work on this as I am talking and to get help from your neighbors.
    I can help with any issues after class.

4. If that's all set up, then click the green "Code" button, click "SSH", and click to copy the command:

    git@github.com:DavisPL-Teaching/119.git

5. Open a terminal and type:

    git clone git@github.com:DavisPL-Teaching/119.git

6. Type `ls`.

    You should see a new folder called "119" in your home folder. This contains the lecture notes and source files for the class.

7. Type `cd `119/lecture1`, then type `ls`.
   Lastly type `python3 lecture.py`. You should see the message below.
"""

print("Hello, ECS 119!")

"""
If some step above didn't work, you may be missing some of the software we
need installed. Please complete HW0 first and then let us know if you
are still having issues.

=== The basics ===

I will introduce the class through a basic overview, or "toy model"
of what a data procesisng pipeline is. Throughout, we will also see
some of the constraints that data processing pipelines have to satisfy,
how they interact with one another, and so on.
This will lead to an overview of topics covered in the class.

Recall "discussion scenarios" from the previous lecture.

EXAMPLE 1:
I have a spreadsheet containing 1000 movies I have seen or want to see,
dates watched, and movie ratings.
I built a Python application which loads the spreadsheet,
filters out movies based on a recently viewed or highest-rated sorting,
and allows me to mark a movie as seen or to edit any movie ratings.
It also collects statistics about all the movies.
All of this data is then saved back to the spreadsheet.

EXAMPLE 2:
I have written a website scraper that reads data from Wikipedia.
I re-run the scraper every week to get the latest data.
It opens up all Wikipedia sites that correspond to cities in the world,
extracts the population of each city, the area, and the country it is located
in. Once all of this data is collected, it stores it in a structured
format and saves it to a database, then queries the database for the
top 100 most population-dense cities and outputs these to a file
biggest_cities.txt.

What are the components of a data processing pipeline?
What do these scenarios have in common?

0.
1.
2.
3.
"""

"""
Step 0: Getting a data source

Useful sites:
- https://ourworldindata.org/data
- sklearn
"""

"""
What are some design constraints or limiting factors that data processing pipelines might have to deal with?

1.
2.
3.
4.

=== Overview of course schedule ===

Overview of the schedule (tentative), posted at:
https://github.com/DavisPL-Teaching/119/blob/main/schedule.md

"""

"""
=== Closing with a quote from Patrice Koehl ===

From [Patrice Koehl](https://www.cs.ucdavis.edu/~koehl/):

    "
        Where is the wisdom we have lost in knowledge?
        Where is the knowledge we have lost in information?
        Where is the information we have lost in data?
    "

    With apologies to T.S. Eliot.
"""
