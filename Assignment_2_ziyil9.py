# Exercise 0
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.


def github() -> str:

    return "https://github.com/Gugu5gun/ECON481/blob/main/Assignment_2_ziyil9.py"

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

    Y = 5 + 3*x_1 + 2*x_2 + 6*x_3 + e
    # Creating the Y array

    X = np.array([x_1,x_2,x_3])
    # Changing this three arrays into a 3D array. 

    result_tuple = (Y,X)
    # Combine it into a tuble, a tuble could be combination of different element.

    return result_tuple

# simulate_data(481)

# Maximize Likelyhood Function

# Write a function that estimates the MLE parameters 
# for data simulated as above, where the assumed model is
# Yi = B0 + B1x1i + B2x1i + B3x1i + e

np.random.seed(481)
# Set seed and testing data set.

x_1 = np.random.normal(0,np.sqrt(2),(1000,1))
x_2 = np.random.normal(0,np.sqrt(2),(1000,1))
x_3 = np.random.normal(0,np.sqrt(2),(1000,1))
e = np.random.normal(0,1,(1000,1))
X = np.array([x_1,x_2,x_3])

y = 5 + 3*x_1 + 2*x_2 + 6*x_3 + e
# Forming the X and y array

initialGuess1 = [1,1,1,1]
# Making an initial guess for the coefficients

def neg_log_likehood(initialGuess1:np.array, X:np.array, y:np.array) -> int:
    
    b0,b1,b2,b3 = initialGuess1
    # Assigning the numbers in initialGuess into the betas

    res = np.zeros((1000,1))
    y_pred = np.zeros((1000,1))
    # Creating the Residual and the Predicted Value of the Y

    y_pred = b0 + b1 * X[0] + b2*X[1] + b3*X[2]
    res = y - y_pred
    # Calculate the 

    likelihood_fun = -np.sum(res**2/2) - 500*np.log(2*np.pi*1)
    # Which is the MLE coefficient

    return - likelihood_fun
    
result = sp.optimize.minimize(neg_log_likehood, initialGuess1, args = (X, y), method = 'Nelder-Mead')

result.x
# To get the coefficient in the result. 

def estimate_mle(y: np.array, X: np.array) -> np.array:
    result_mle = np.array(result.x)
    return result.reshape(-1,1)

# estimate_mle(y,X)
# Credicts to my friend:Francis (Discord Id) 


initialGuess1 = [1,1,1,1]

def get_sqrres(initialGuess1:np.array, X:np.array, y:np.array) -> int:
    
    b0,b1,b2,b3 = initialGuess1
    # Assigning the numbers in initialGuess into the betas

    res = np.zeros((1000,1))
    y_pred = np.zeros((1000,1))
    # Creating the Residual and the Predicted Value of the Y

    y_pred = b0 + b1 * X[0] + b2*X[1] + b3*X[2]
    res = y - y_pred
    # Calculate the residual

    res = res**2
    # Get the squared residual

    return np.sum(res)
    
result = sp.optimize.minimize(get_sqrres, initialGuess1, args = (X, y))
# The sp.optimize.minizie work in following way:
# It takes in a value return by a function, a set of initial guess numbers, and arguments about
# Which datasets are going to be included in. Afterward, this function will try to fill in the 
# Initial Guess with different values, until it could get a minimum value in result of get_res.

def estimate_ols(y: np.array, X: np.array) -> np.array:
    result_coe = np.array(result.x)
    return result_coe

