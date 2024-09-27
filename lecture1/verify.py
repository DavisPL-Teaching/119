import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import pyspark.sql as sql

def verify():
    print()
    print("Python version:", sys.version)
    print("Numpy version:", np.__version__)
    print("Pandas version:", pd.__version__)
    print("Matplotlib version:", plt.matplotlib.__version__)
    print()

    # Simple numpy and pandas operations to verify functionality
    # - Create a numpy array
    array = np.array([1, 2, 3])
    print("Numpy array:", array)

    # - Add stuff to the array
    array = array + 4
    print("Numpy array after addition:", array)

    # - Make a pandas DataFrame
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    print("Pandas DataFrame:\n", df1)
    print()

    # A basic pyspark test
    spark = sql.SparkSession.builder.appName("Verify").getOrCreate()
    df2 = spark.createDataFrame([
        sql.Row(a=1, b=2., c='string1'),
        sql.Row(a=2, b=3., c='string2'),
        sql.Row(a=4, b=5., c='string3'),
    ])
    df2.show()
    print("Spark version:", spark.version)
    print()

    # Plot the first DataFrame using matplotlib
    plt.plot(df1)
    plt.show()

if __name__ == "__main__":
    verify()
