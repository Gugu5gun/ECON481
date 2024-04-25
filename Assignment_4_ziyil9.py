import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import statsmodels.api as sm
from datetime import datetime

# This HW response used a package "statsmodels.api"
# Ref: https://www.statology.org/ols-regression-python/#:~:text=How%20to%20Perform%20OLS%20Regression%20in%20Python%20%28With,Step%203%3A%20Visualize%20the%20Line%20of%20Best%20Fit

from sklearn.linear_model import LogisticRegression
# This HW used the "scikit-learn" package, Please make sure you have used pip install scikit-learn to install the required packages. 
# Ref: https://www.statology.org/logistic-regression-python/#:~:text=How%20to%20Perform%20Logistic%20Regression%20in%20Python%20%28Step-by-Step%29,Model%20...%205%20Step%205%3A%20Model%20Diagnostics%20


# Excersise 0
def github() -> str:

    return "https://github.com/Gugu5gun/ECON481/blob/main/Assignment_4_ziyil9.py"

# Excersise 1
# Please write a function called load_data that accesses the file on 
# Tesla stock price history on the course website and returns that data as a pd.DataFrame.
# Use the following shell:

def load_data() -> pd.DataFrame:
   
    tesla_csv = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')
    # Read the CSV file with given link as the dataframe. 

    return tesla_csv

# Excersise 2
# Please write a function called plot_close which takes the output of load_data() 
# as defined above, as well as an optional start and end date (strings formatted as ‘YYYY-MM-DD’)
# and plots the closing price of the stock between those dates as a line graph. 
# Please include the date range in the title of the graph. 
# Note that this function needn’t return anything, just plot a graph using matplotlib.
# Use the following shell:

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:

    df_test = df
    # Assign the df to a new dataframe, to avoid modifiying the orginial document.
    
    df_test['Date'] = pd.to_datetime((df_test['Date']))
    # Convert the date column into datetime, so we can filter it with given period. 

    format = '%Y-%m-%d'
    # Building the regular experession for the date format in the csv file.

    time_start = datetime.strptime(start,format)
    time_end = datetime.strptime(end,format)
    # Transform both the starting date and ending datge into the datetime format.

    df_test = df_test[(df_test['Date'] >= time_start) & (df_test['Date'] <= time_end)]
    # Filter the df file with the period we want

    plt.plot(df_test['Date'],df_test['Close'],color = "black")
    plt.xlabel('Date (in Years)')
    plt.ylabel('Closing Price (in USD)')
    plt.title('Closing Prices Throughout Years')
    # Build the plot, with X axis with date, and Y axis with the closing price.

    plt.show()
    # Show the graph of the plot. 

# df = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')
# plot_close(df, start='2010-06-29', end='2024-04-15')
# For test purpose code, the output is correct. Based on the test, the str after could also be other time points.
# Such as plot_close(df, start='2018-04-25', end='2020-04-25') would show the changes along the period. 

# Excersise 3
# Please write a function called autoregress that takes a single argument df (the output of Exercise 1) 
# and returns the t statistic on B0 from the regression

def autoregress(df: pd.DataFrame) -> float:

    df_test = df
    # Avoid to change the orginial dataframe

    df_test['Close_Pre'] = df_test['Close'].shift(1)
    # Credicts to https://www.geeksforgeeks.org/python-pandas-dataframe-shift/ Which told me about this function
    # By doing this, we can have the previous day closing prices in the new column

    df_test['Close_Pre'] = df_test['Close_Pre'].fillna(0)
    # Fill the NaNs in the dataframe with 0 to avoid error. 

    df_test['Delta_Closing'] = df_test['Close'] - df_test['Close_Pre']
    # Getting the "DELTA X" values for the OLS model 

    y = df_test['Delta_Closing']
    x = df_test['Close_Pre']
    # Get the dependent variable and independent variables for OLS regression

    x = sm.add_constant(x)
    # I dont know why I should add this part of "add_constant"
    # I guess it is used to make X, the Close_Pre, to a regressor 

    E3_Model = sm.OLS(y, x)
    # Apply the OLS model on Y based on X

    t_stat = E3_Model.fit(cov_type='HC1').tvalues[1]
    # As the Question asked, use the "HC1" standard errors for the regression. 

    return t_stat

# df = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')
# result_test = autoregress(df)
# For testing purpose

# Exercise 4
# Let’s specify the analysis slightly differently. 
# Please write a function called autoregress_logit that takes a single argument df (the output of Exercise 1)
# and returns the t statistic on B0 from the logistic regression.

def autoregress_logit(df: pd.DataFrame) -> float:

    df_test = df

    df_test['Close_Pre'] = df_test['Close'].shift(1)
    # Credicts to https://www.geeksforgeeks.org/python-pandas-dataframe-shift/ Which told me about this function
    # By doing this, we can have the previous day closing prices in the new column

    df_test['Close_Pre'] = df_test['Close_Pre'].fillna(0)
    # Fill the NaNs in the dataframe with 0 to avoid error. 

    df_test['Delta_Closing'] = df_test['Close'] - df_test['Close_Pre']
    # Same as the codes used in the Exercise 3.
    
    y = df_test['Delta_Closing']
    X = df_test['Close_Pre']

    y = y.loc[X.index]
    # I dont know why should I add this part into the code, I refered to my friend's code. 
    # He told me this is used to prevent error??

    model = sm.Logit((y > 0).astype(int) , X)
    # Make the logistic regression.
    
    t_stat = model.fit()
    t_output = t_stat.tvalues
    # Get the t_statistic.

    return t_output


# df_test = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')
# test_result = autoregress_logit(df_test)
# For test purpose only

# Exercise 5
# Please write a function called plot_delta that takes a single argument df (the output of Exercise 1) and plots 
# for the full dataset. Note that this function needn’t return anything, just plot a graph using matplotlib.

def plot_delta(df: pd.DataFrame) -> None:
 df_test = df
 df_test['Close_Pre'] = df_test['Close'].shift(1)
 df_test['Close_Pre'] = df_test['Close_Pre'].fillna(0)
 df_test['Delta_Closing'] = df_test['Close'] - df_test['Close_Pre']
 df_test['Date'] = pd.to_datetime((df_test['Date']))

 plt.plot(df_test['Date'],df_test['Delta_Closing'],color = "red",linewidth=0.5)
 plt.xlabel('Date (in Days)')
 plt.ylabel('Amount of Changes in Price (in USD)')
 plt.title('The Trend of price floating Throughout Years')
 plt.show()


# plot_delta(df)
# Based on this graph, we could find that, when a company become more and more successful,
# It is likely that the stock price would have a bigger range of variation. 
# I feel like this is caused by the reason that, the inverstors are likely to hold large amount of stocks
# of the giant companies like TESLA, and use them for loan collateral or offering options.

# Yet, it is also possible that, when every inverstor is trying to predict the CHOICES OF THE "GROUP" which they are already A PART OF IT,
# The result of the trend would just become LESS PREDICTABLE. 
# Which is more reasonable. Everyone wants to predict others, but eventually nobody actually could. 

