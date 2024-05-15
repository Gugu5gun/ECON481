import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session
# Import the needed package

path = 'E:/ECON481/auctions.db'
engine = create_engine(f'sqlite:///{path}')
# 
#
# 
# Please change the path for furthuer verification!!!!
#
#
#

from sqlalchemy import inspect
inspector = inspect(engine)
inspector.get_table_names()
# Returns ['bids', 'items'], we are getting correct data.

def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<user>/<repo>/blob/main/<filename.py>"

# Please write a function called std that takes no arguments and returns a string containing a SQL query
# that can be run against the auctions.db database that outputs a table that has two columns: itemId and std,
# the standard deviation of bids for that item. Include only bids for which the unbiased standard deviation
# can be calculated (that is, those with at least two bids). Calculate standard deviation as following:

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def inspect(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)
    
# Reference: https://lukashager.netlify.app/econ-481/07_sql#/writing-a-query-class

df_auctions = DataBase(path)
q = 'select * from bids'
# print(df_auctions.inspect(q).tail())

# 使用unique方法，获取到底有多少个itemID，对每一个itemID做一个单独的dataframe来计算mean和std
# Using the idea of "Unique" to know the content and number of item ID. 
# For each itemID, make a specific dataframe to calculate mean and std

def std() -> str:

    df_bids = pd.read_sql_query(q, engine)
    # Get the "bids" dataframe
    df_item_ID = df_bids.itemId
    freq = df_item_ID.value_counts()
    # use this one to know the frequency of appearence 
    
    freq_filtered = freq[freq > 2]
    # for each item. Then we have to remove those items appears less than 2 times. 

    freq_filtered = freq_filtered.reset_index()
    freq_filtered = freq_filtered.rename(columns={'index': 'itemID', 'itemID': 'bid_time'})
    # To make the data more accessible, so we could make the left join and do the filter! 
    
    df_test = pd.merge(df_bids, freq_filtered, on='itemId', how='inner')
    # Now we have a specific column named "bidCount" to represent the number of bids for each item.
    # By using the 'inner' join function, only the ones with 2 bids and more will be remain

    df_by_id = df_test.groupby('itemId')
    # Then, we could group the bids by itemID

    bid_mean = df_by_id['bidAmount'].mean()
    bid_std = df_by_id['bidAmount'].std()
    # Calculate the mean and std of each item

    bid_data = pd.merge(bid_mean,bid_std, on='itemId', how='inner')
    # Merge the data together to make the output

    bid_data  = bid_data .reset_index()
    bid_data  = bid_data .rename(columns={'bidAmount_x': 'bid_mean', 'bidAmount_y': 'bid_std'})
    # Rename the data for more readibility

    print(bid_data)
    # Return the result. 
    return None

query = """
    SELECT 
        itemId,SQRT(SUM((bidAmount - avg_bidAmount) * (bidAmount - avg_bidAmount)) / (COUNT(bidAmount) - 1)) as std
    FROM 
        (SELECT 
            itemId, 
            bidAmount, 
            AVG(bidAmount) OVER (PARTITION BY itemId) AS avg_bidAmount 
        FROM 
            bids) subquery
    GROUP BY 
        itemId
    HAVING 
        COUNT(bidAmount) > 1;
    """

# To deal with this question, we should first found those datas appears more than 2 times
# Which we should filter the ones with bidAmount greater than 2. 
# Ref: https://learnsql.com/blog/partition-by-with-over-sql/

query = """
    SELECT itemId
    FROM(
    SELECT itemId,bidAmount,COUNT(*) as bid_count, AVG(bidAmount) OVER (PARTITION BY itemID) as avg_bid
    FROM bids
    GROUP BY itemId
    HAVING COUNT(bidAmount) > 2
    )

    """


query = """
    SELECT 
        itemId,
        SQRT(SUM((bidAmount - avg_bidAmount) * (bidAmount - avg_bidAmount)) / (COUNT(bidAmount) - 1)) as std
    FROM 
        (SELECT 
            itemId, 
            bidAmount, 
            AVG(bidAmount) OVER (PARTITION BY itemId) AS avg_bidAmount 
        FROM 
            bids) subquery
    GROUP BY 
        itemId
    HAVING 
        COUNT(bidAmount) > 1;
    """

# SQRT(SUM((bidAmount - avg_bid) * (bidAmount - avg_bid)) / (COUNT(bidAmount) - 1)) as std

df_bids = pd.read_sql_query(query, engine)

# Please write a function called bidder_spend_frac that takes no arguments
# and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has four columns:

# bidderName: the name of the bidder
# total_spend: the amount the bidder spent (that is, the sum of their winning bids)
# total_bids: the amount the bidder bid, regardless of the outcome. NB: bidders may submit multiple bids for an item – if this is the case only count their highest bid for an item for this calculation.
# spend_frac: total_spend/total_bids

df_bids = pd.read_sql_query(q, engine)
df_items = pd.read_sql_query("select * from items", engine)
df_item_ID = df_bids.isBuyerHighBidder
freq = df_item_ID.value_counts()

df_test = pd.read_sql_query('SELECT bidderName, itemId, MAX(itemPrice) AS total_bids FROM bids GROUP BY bidderName', engine)

names = df_bids.bidderName
print(names.value_counts())

pd.read_sql_query()