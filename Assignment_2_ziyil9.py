# Exercise 0
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.


def github() -> str:

    return "https://github.com/Gugu5gun/ECON481/Assignment_2_ziyil9.py"

import numpy as np
import scipy as sp

# Exercise 1
# Please write a function that returns 1000 simulated observations via the following data generating process:
# Yi = 5 + 3*x1 + 2*x2 + 6*x3 + e

def simulate_data(seed: int) -> tuple:

    if seed == None:
        seed = 481

    np.random.seed(seed)
    x_1 = np.random.normal(0,np.sqrt(2),(1000,1))
    x_2 = np.random.normal(0,np.sqrt(2),(1000,1))
    x_3 = np.random.normal(0,np.sqrt(2),(1000,1))
    e = np.random.normal(0,1,(1000,1))
    # Which means that, draw 1000 samples from a normal distribution with mean of 0 and SD of 2
    # y = np.zeros((1000,1))

    Y = 5 + 3*x_1 + 2*x_2 + 3*x_3 + e
    # Creating the Y array

    X = np.array([x_1,x_2,x_3])
    # Changing this three arrays into a 3D array. 

    result_tuple = (Y,X)
    return result_tuple

# simulate_data(481)

# Start from here, for test only

# X_1 = np.random.normal(0,np.sqrt(2),(3,1))
# X_2 = np.random.normal(0,np.sqrt(2),(3,1))
# e = np.random.normal(0,1,(3,1))

# X = np.array([X_1,X_2])

# Y = X_1 + X_2 + e + 2

# result_tuple = (Y,X)

# Ending part of testing...

# Write a function that estimates the MLE parameters 
# for data simulated as above, where the assumed model is
# Yi = B0 + B1x1i + B2x1i + B3x1i + e

def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """

    return None
