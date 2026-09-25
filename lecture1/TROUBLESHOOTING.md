# Troubleshooting

Some tips for if you are having trouble with running the lecture files, or with Homework 0.

### Windows issues

1. If you are on Windows, in our experience, many of the installation issues are common and specific to Windows machines. In this case, I highly recommend that you avoid the issues entirely by installing Windows Subsystem for Linux (WSL) and doing your development work there. The following guide will walk you through:

    [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

    WSL is basically a Linux system inside your Windows system, and it works very well. It's used very commonly by developers.

    If you only have issues on the last step of HW0 (Spark), you could just use WSL for that part, for example.

2. To get access the HW0 form (and all other forms in the class), you will need to log in with your UC Davis email - please make sure you are logged in with the same email for all forms! Don't send a request to access the form from a non-UCD email, as we won't be able to grant that.

You should aim to resolve all installation issues by Wednesday - Wednesday's discussion section can help with installation. I am also happy to help out with installation in office hours.

#### Another note -- use WSL, downgrade to Java 11 (from the TA):

For those of you who are having errors on windows: last year we were able to resolve this for many of you by downgrading to Java 11, openjdk 11.0.x should fix it. Anyone getting

```
raise Py4JJavaError(
        "An error occurred while calling {0}{1}{2}.\n".
        format(target_id, ".", name), value)
py4j.protocol.Py4JJavaError: An error occurred while calling o47.showString.
```

is because of that.

### PySpark

You will need PySpark working for the latter part of the course. We found that:
  - for Windows, Java 11, Python 3.12.3, Pyspark 3.5.3 work
  - for Mac/WSL: Java 21 or 22 works.
