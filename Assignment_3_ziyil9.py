import pandas as pd
import numpy as np
# Import the needed data

# Excersize 0
def github() -> str:

    return "https://github.com/Gugu5gun/ECON481/blob/main/Assignment_3_ziyil9.py"


# Exercise 1
# Please write a function called import_yearly_data that takes as its argument a list of years 
# and returns a concatenated DataFrame of the Direct Emitters tab of each of those year’s EPA excel sheet.
# Please add a variable year that references the year from which the data is pulled. Please use the fourth row as the column names
# and do not import the first three rows. Do not use any columns as an index.

def import_yearly_data(years: list) -> pd.DataFrame:

    years = list(set(years))
    # Make sure the years will be unique.

    i = range(len(years))
    output_yr = pd.DataFrame()
    # Set up an empty dataframe to fill in data.

    for j in i:
        if years[j] == 2019:
            current_yr = pd.read_excel('https://lukashager.netlify.app/econ-481/data/ghgp_data_2019.xlsx',sheet_name= 'Direct Emitters',skiprows = 3)
        elif years[j] == 2020:
            current_yr = pd.read_excel('https://lukashager.netlify.app/econ-481/data/ghgp_data_2020.xlsx',sheet_name= 'Direct Emitters',skiprows = 3)
        elif years[j] == 2021:
            current_yr = pd.read_excel('https://lukashager.netlify.app/econ-481/data/ghgp_data_2021.xlsx',sheet_name= 'Direct Emitters',skiprows = 3)
        else:
            current_yr = pd.read_excel('https://lukashager.netlify.app/econ-481/data/ghgp_data_2022.xlsx',sheet_name= 'Direct Emitters',skiprows = 3)
        # If else statements, based on the content in the list to choose the xlsx file needed. 
        current_yr['year'] = years[j]
        output_yr = pd.concat([output_yr,current_yr], ignore_index=True)    
    
    return output_yr

# Exercise 2
# Please write a function called import_parent_companies that takes as its argument a list of years
# and returns a concatenated DataFrame of the corresponding tabs in the parent companies excel sheet1. 
# Please add a variable year that references the year from which the data is pulled. 
# Finally, please remove any row that is entirely null values. Do not use any columns as an index.

def import_parent_companies(years: list) -> pd.DataFrame:
    
    output_yr = pd.DataFrame()
    # Setting up an empty dataframe for output

    url = 'https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb'
    # Setting the URL for accessing the data.
    years = list(set(years))
    i = range(len(years))

    for j in i:
        current_yr = pd.read_excel(url,str(years[j]),engine='pyxlsb')
        # Assign the ghgp data into a temporary "current data"
        current_yr = current_yr.dropna(how = 'all')
        # Remove the lines with NA.
        current_yr['year'] = years[j]
        # Adding a "year" column to the current data
        output_yr = pd.concat([output_yr,current_yr])
        # Adding up the "current data" to the base data output_yr

    return output_yr

# test_1 = import_yearly_data([2019,2020,2021,2022])

# Exercise 3
# Please write a function called n_null that takes as its arguments a DataFrame and a column name
# and returns an integer corresponding to the number of null values in that column. Use the following shell:

def n_null(df: pd.DataFrame, col: str) -> int:
    column_needed = df[col]
    # Narrow down the orginial dataframe to only one column
    num_NA = column_needed.isna().sum()
    # Getting the number of null and NAs in the column
    return int(num_NA)

# Exercise 4
# Please write a function called clean_data that takes as its arguments a concatenated DataFrame
#  of emissions sheets (the output of Exercise 1) and a concatenated DataFrame of parent companies 
# (the output of Exercise 2) and outputs a DataFrame produced using the following steps:

def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:

    merged_df = pd.merge(emissions_data,parent_data, left_on=['year','Facility Id' ], right_on=['year','GHGRP FACILITY ID' ], how='left')
    # Merging the data together based on "year" and "ID". Since the name of ID is different, 
    # we have to use multiple arguments to make the left join. In here, we take GHGRP FACILITY ID equvialent to Facility Id. 
    merged_df = merged_df[['Facility Id', 'year','State','Industry Type (sectors)','Total reported direct emissions','PARENT CO. STATE','PARENT CO. PERCENT OWNERSHIP']]
    # Subset the column into the ones we need
    merged_df = merged_df.rename(columns={col: col.lower() for col in merged_df.columns})
    # Change the name of column into all lower cases

    return merged_df


# df_test = clean_data(import_yearly_data([2019,2020,2021,2022]),import_parent_companies([2019,2020,2021,2022]))
# Testing rounds.

# Exercise 5
# Please write a function called aggregate_emissions that takes as input a DataFrame with the schema 
# of the output of Exercise 4 and a list of variables and produces the minimum, median, mean, 
# and maximum values for the following variables (note the case change) aggregated at the level of the variables supplied in the argument:

def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    
    Variables = ['total reported direct emissions','parent co. percent ownership']
    output_df = df.groupby(group_vars,as_index=True)[Variables].agg(['min','median','mean','max'])

    return output_df

# Credicts to my friend on Exercise 5: Francis (Discord Id)

# df_test = aggregate_emissions(clean_data(import_yearly_data([2019,2020]),import_parent_companies([2019,2020])),['year'])
# test rounds