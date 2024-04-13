# Import packages
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import sqlite3

# Fetch the data
def fetch_book_data(url : str, max : int = 51):
    data = []
    i = 1
    while (True | i<max):
        try:
            page_numerator = f"/catalogue/page-{i}.html"
            page = requests.get(url + page_numerator).text
            soup = bs(page)
            item_list = soup.find_all("article")
            for item in item_list:
                rows = {}
                rows["title"] = item.find("h3").find("a")["title"]
                rows["star_rating"] = item.find("p")["class"][1]
                rows["url"] = url + item.find("a")["href"]
                rows["price_in_pounds"] = item.find("p", attrs = {"class" : "price_color"}).getText()[2:]
                rows["availability"] = item.find("p", attrs = {"class" : "instock availability"}).getText()
                data.append(rows)
            print(f"Page {i} - ({len(item_list)} of {len(data)})")
            i+=1
        except:
            break
    return data

# Clean & Format the data
def format_book_data(data : list):
    # Save data as book_df
    book_df = pd.DataFrame(data)
    ## Format 'price_in_pounds' column as float
    book_df["price_in_pounds"] = book_df["price_in_pounds"].astype("float")
    ## Create 'rating' columnn as numerical map of 'star_rating' column
    book_df["rating"] = book_df["star_rating"].replace(
        {
            "One" : 1,
            "Two" : 2,
            "Three" : 3,
            "Four" : 4,
            "Five" : 5
        }
    ).fillna(0)
    ## Clean 'availability' column
    book_df["availability"] = book_df["availability"].str.replace("\n", "").str.strip()
    ## Create 'is_available' column from 'availability' column
    book_df["is_available"] = book_df["availability"].replace({"In stock": True}).fillna(False)
    ## Drop 'star_rating' and 'is_available' columns
    book_df = book_df.drop(columns=["star_rating", "availability"])
    return book_df

# Load the data
def load_book_data(book_df : pd.DataFrame):
    # Connect to the database
    con = sqlite3.connect("book_store.db")
    cur = con.cursor()
    # Drop the table if exist
    # create table
    stmt = """
    DROP TABLE IF EXISTS master_books;
    """
    cur.execute(stmt)
    # Create the table
    stmt = """
    CREATE TABLE IF NOT EXISTS master_books(
        title varchar,
        url text,
        price_in_pounds float,
        rating int,
        is_available boolean
    );
    """
    cur.execute(stmt)
    # Insert data
    cur.executemany(
        "INSERT INTO master_books values(?,?,?,?,?)",
        book_df.itertuples(index=False, name=None)
    )
    con.commit()

# Check the data
def check_book_data(cur, stmt : str):
    data = cur.execute(stmt).fetchall()
    for d in data:
        print(d)