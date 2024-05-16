import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import inspect
# Import the needed package

path = 'E:/ECON481/auctions.db'
engine = create_engine(f'sqlite:///{path}')

# 
# 
# Please change the path for furthuer verification!!!!
# 
# 

review = inspect(engine)
review.get_table_names()
# Returns ['bids', 'items'], we are getting correct data.

def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/Gugu5gun/ECON481/blob/main/Assignment_6_ziyil9.py"

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

"""
def std() -> str:

    df_bids = pd.read_sql_query(q, engine)
    # Get the "bids" dataframe
    df_item_ID = df_bids.itemId
    freq = df_item_ID.value_counts()
    # use this one to know the frequency of appearence 
    
    freq_filtered = freq[freq > 1]
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

# """
# This was an attempt of doing so without sql query
# Which make me finds that, when the freq (which means the number of BidAmount) is greater than 2
# There will be not zeros in the bid_std
# But if I set this value as "greater than 1", there will be not zeros in the bid_std
# The zero in std is caused by an ite with itemId "172998011", which two users had same bid amount.

# To deal with this question, we should first found those datas appears more than 2 times
# Which we should filter the ones with bidAmount greater than 2. 
# Ref: https://learnsql.com/blog/partition-by-with-over-sql/

def std() -> str:
    query = """
    SELECT 
        itemId,
        SQRT(SUM((bidAmount - avg_bid) * (bidAmount - avg_bid)) / (COUNT(bidAmount) - 1)) as std
    FROM 
        (SELECT 
            itemId, 
            bidAmount, 
            AVG(bidAmount) OVER (PARTITION BY itemId) AS avg_bid 
        FROM 
            bids) subquery
    GROUP BY 
        itemId
    HAVING 
        COUNT(bidAmount) > 1;
    """
    return query

# SQRT(SUM((bidAmount - avg_bid) * (bidAmount - avg_bid)) / (COUNT(bidAmount) - 1)) as std

df_bids = pd.read_sql_query(std(), engine)

# Please write a function called bidder_spend_frac that takes no arguments
# and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has four columns:
# bidderName: the name of the bidder
# total_spend: the amount the bidder spent (that is, the sum of their winning bids)
# total_bids: the amount the bidder bid, regardless of the outcome. NB: bidders may submit multiple bids for an item – if this is the case only count their highest bid for an item for this calculation.
# spend_frac: total_spend/total_bids

def bidder_spend_frac() -> str:
    """
    Returns a string containing a SQL query that can be run against the auctions.db database 
    that outputs a table that has four columns:
    bidderName, total_spend, total_bids, spend_frac: total_spend/total_bids.
    """
    query = '''
    WITH MaxBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS max_bid --Select 
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    TotalSpend AS (
        SELECT 
            bidderName, 
            SUM(max_bid) AS total_spend
        FROM 
            MaxBids
        GROUP BY 
            bidderName
    ),
    BidAmount AS (
        SELECT 
            bidderName, 
            MAX(bidAmount) AS bids_amt
        FROM 
            bids
        GROUP BY 
            bidderName, itemId  -- Group by itemId to find the maximum bid for each bidder on each item
    ),
    TotalBids AS (
        SELECT
            bidderName,
            SUM(bids_amt) AS total_bids
        FROM
            BidAmount
        GROUP BY
            bidderName
    )       
    SELECT 
        ts.bidderName,
        ts.total_spend,
        tb.total_bids,
        CASE
            WHEN tb.total_bids > 0 
            THEN ts.total_spend * 1.0 / tb.total_bids
            ELSE 0
        END AS spend_frac
    FROM 
        TotalSpend ts
    JOIN 
        TotalBids tb ON ts.bidderName = tb.bidderName;
    '''
    return query

# Excersize 3
# I dont know how to use the SQL in python, but I have abstract ideas about how to doing so.
# First, I will make a left join from "items" table into the "bids" table,
# At this time, for each "itemId", there would be a "bidIncrement" value attched to it.
# Then, we add a new column named "IsBidMin" into the dataframe. Which euqals to 1 when the "BidAmount" equals to "bidIncrement"
# Such as, if the "bidIncrement" = 1, and BidAmount = 2, the "IsBidMin" would be false, because "Bid"

def min_increment_freq() -> str:
    """
    
    """
    
    query = """
    SELECT 
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM bids WHERE itemId IN (SELECT itemId FROM items WHERE isBuyNowUsed = 0)) AS freq
    FROM 
        bids b1
    JOIN 
        items i ON b1.itemId = i.itemId
    WHERE 
        i.isBuyNowUsed = 0
        AND b1.bidAmount = (
            SELECT MAX(b2.bidAmount)
            FROM bids b2
            WHERE b2.itemId = b1.itemId 
                AND b2.bidTime < b1.bidTime
        ) + i.bidIncrement;
    """
    return query

# For this sql, we could use the order by timer and by itemId to achieve a similar result. 
# But after dicussion, we found it will make the code more complicated, so we decided not to use it. 

def win_perc_by_timestamp() -> str:
    """
    Docstring
    """

    query = """
    WITH AuctionTimes AS (
        SELECT
            itemId,
            MIN(bidTime) AS auctionStartTime,
            MAX(bidTime) AS auctionEndTime
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    BinnedBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.bidAmount,
            ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
            (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) AS normalized_time,
            CASE
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.1 THEN 1
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.2 THEN 2
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.3 THEN 3
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.4 THEN 4
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.5 THEN 5
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.6 THEN 6
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.7 THEN 7
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.8 THEN 8
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin
        FROM
            bids b
        JOIN
            AuctionTimes a ON b.itemId = a.itemId
    ),
    MaxBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS max_bid
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    BinnedWinningBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.timestamp_bin
        FROM
            BinnedBids b
        JOIN
            MaxBids w ON b.itemId = w.itemId AND b.bidAmount = w.max_bid
    )
    SELECT
        timestamp_bin,
        COUNT(b.itemId) * 1.0 / (SELECT COUNT(*) FROM BinnedBids WHERE BinnedBids.timestamp_bin = b.timestamp_bin) AS win_perc
    FROM
        BinnedWinningBids b
    GROUP BY
        timestamp_bin;
    """
    return query