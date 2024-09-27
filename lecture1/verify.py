import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

def verify():
    print("Python version:", sys.version)
    print("Numpy version:", np.__version__)
    print("Pandas version:", pd.__version__)

    # Simple numpy and pandas operations to verify functionality
    array = np.array([1, 2, 3])
    print("Numpy array:", array)

    # Add stuff to the array
    array = array + 4
    print("Numpy array after addition:", array)

    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    print("Pandas DataFrame:\n", df)

    # Make a plot using matplotlib
    plt.plot(array)
    plt.show()

if __name__ == "__main__":
    verify()
