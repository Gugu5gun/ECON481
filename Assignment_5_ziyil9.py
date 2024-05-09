import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
# import re

# Exercise 0
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.

def github() -> str:

    return "https://github.com/Gugu5gun/ECON481/blob/main/Assignment_5_ziyil9.py"

# Exercise 1
# Please write a function called scrape_code that takes as its argument a lecture’s URL on the course website 
# (the HTML format, so, for example, https://lukashager.netlify.app/econ-481/01_intro_to_python) and returns 
# a string containing all the python code in the lecture formatted in such a way that we could save it 
# as a python file and run it without syntax issues (note that if you try to do actually run the file, 
# you’ll likely hit some syntax issues since there some that exist by construction in the presentations).

def scrape_code(url: str) -> str:

    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    # Adding headers in case the request is rejected.
    url_result = requests.get(url,headers = headers)
    # Making a request to the website, and return the data.

    if url_result.ok != True:
        return "Failure to Access the website"

    url_bs = BeautifulSoup(url_result.text, "html.parser")
    # Using the "html parser" as the decoder

    python_codes = url_bs.find_all('code', attrs={'class': 'sourceCode python'})
    # By using inspect, we found <code class="sourceCode python"> appears above the codes
    # The type of the class is "sourceCode python". With "code" in front

    output_code = ''

    for python_code in python_codes:
        # Making a loop to find all "Python codes" that matched the pattern

        code_in_page = python_code.get_text()
        seperate_codes = code_in_page.split('\n') # This line of code is modified by my friend
        filtered_codes = '\n'.join([code for code in seperate_codes if not code.startswith('%')]) # So do this line. 
        # Yet, we still need to clean the codes to avoid the codes from another language
        # If it is starting with a %, then igrone it. Else, adding it to the output codes 
        output_code += filtered_codes + '\n'
    


    return '"' + output_code + '"'
    # return the output wtih "" 

#print(scrape_code("https://lukashager.netlify.app/econ-481/01_intro_to_python#/lists"))
print(scrape_code('https://lukashager.netlify.app/econ-481/02_numerical_computing_in_python#/basic-problem-lists'))

# Reference：https://www.youtube.com/watch?v=QhD015WUMxE

# Just Another Practice I made to practice the scraping 

# url = 'https://movie.douban.com/chart'
# headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
# response = requests.get(url,headers = headers)
# print(response)
# html_str = response.text
# pattern = re.compile('<a.*?nbg.*?title="(.*?)">',re.S)
# items = re.findall(pattern,html_str)
# print(items)


