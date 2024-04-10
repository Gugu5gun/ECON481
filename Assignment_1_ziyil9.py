# Exercise 0
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.

def github() -> str:

    return "https://github.com/Gugu5gun/ECON481"
# I still dont know how to set up Github yet...


# Exercise 1
# Please ensure that you can run python1, can use Git, and install the following packages2 (we’ll install more as we go):
# numpy
# pandas
# scipy
# matplotlib
# seaborn

# !!! pip install has to be used in the terminal, NOT INSIDE IDE. !!!
# All the Packages is intalled. 

# Exercise 2
# Please write a function called evens_and_odds that takes as argument a natural number n and returns a dictionary with two keys, “evens” and “odds”. 
# “evens” should be the sum of all the even natural numbers less than n, and “odds” the sum of all natural numbers less than n.

def evens_and_odds(n:int) -> dict:

    all_num_lst = [0] * n
    j = 0
    even_sum = 0
    odd_sum = 0
    output = {'evens':even_sum, 'odds':odd_sum}
    # Build up an empty list with the length of j to storage the numbers smaller than n

    for j in range(n - 1):
        all_num_lst[j] = j + 1
        if (all_num_lst[j] %2 == 0):
            even_sum += all_num_lst[j]
        else:
            odd_sum += all_num_lst[j]
        j = j + 1
    # For loop how to set up a deafult value for str in pythoni

    output['evens'] = even_sum
    output['odds'] = odd_sum
    return output
    
# Credicts to Semed, who explained me about how the 'dict' part works 

# Please write a function called time_diff that takes as arguments two strings in the format ‘YYYY-MM-DD’ and a keyword out dictating the output.
# If the keyword is “float”, return the time between the two dates (in absolute value) in days. 
# If the keyword is “string”, return “There are XX days between the two dates”. 
# If not specified, the out keyword should be assumed to be “float”. You should use the datetime package, and no others.

from typing import Union
from datetime import datetime, date, time, timedelta

def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    if out == None:
        out = "float"
    # Set up the deafult value for out

    date_a = datetime.strptime(date_1, '%Y-%m-%d')
    date_b = datetime.strptime(date_2, '%Y-%m-%d')
    delta = date_b - date_a
    # Convert the str into the form of datetime. 
    output_days =  delta.days
    output_days = int(output_days)
    # Once we get the difference, we use .days to convert it into a str of days
    # Then, we use the int() function to make it able to output as a int. 

    if out == "float":
        return abs(output_days)
    else:
        return "There are " + str(output_days) + " days between the two dates."
    # It seems like that Python cannot combine int and str together, so I made the output_days back to str form again. 
        

# Exercise 4
# Please write a function called reverse that takes as its argument a list and returns a list of the arguments in reverse order (do not use any built-in sorting methods).

# For example, reverse(['a', 'b', 'c']) should return
# ['c', 'b', 'a']

def reverse(in_list: list) -> list:

    list_size = len(list)
    # Getting the size of the list inputted

    list_reversed = ['a'] * list_size
    # Create a list that used to output the reversed order

    for i in range(list_size):
        list_reversed[list_size - i - 1] = list[i]
    # Use a for loop to rearrange the sequence

    return(list_reversed)   

# Exercise 5
# Write a function called prob_k_heads that takes as its arguments natural numbers n and k with n>k and returns the probability of getting k heads from n flips.

# For example, prob_k_heads(1,1) should return .5

def prob_k_heads(n: int, k: int) -> float:

    prob = 0.5
    n_fac = 1
    k_fac = 1
    n_min_k_fac = 1

    for num in range(1, n + 1):
        n_fac *= num
    
    for num in range(1, k + 1):
        k_fac *= num

    for num in range(1, n - k + 1):
       n_min_k_fac *= num
    

    bio_coe = n_fac / (k_fac * n_min_k_fac)

    prob_heads = bio_coe * (prob ** k) * (1 - prob) ** (n - k)

    return prob_heads
# I believe there could be a more effective way to calculate the coefficients.

