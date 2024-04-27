# Simple Data Scraping From A Bookstore

This is a simple end-to-end ETL project about a scraping data from a [bookstore](https://books.toscrape.com) and store the data to an ```SQLite``` database.

This project build on ```Python``` scripts, mainly using ```request``` and [```Beautiful Soup```](https://beautiful-soup-4.readthedocs.io/en/latest/) library to pull and parse the ```HTML``` of the web pages. ```Pandas``` is used to clean and organize the data before submit it to the database.

## Workflow

```mermaid
flowchart LR
    extract["`Fetch and Parse the data using _request_ and _Beautiful Soup_`"]
    transform["`Format the data type and clean the data using _Pandas_`"]
    load["`Load the data type into _book_store.db_`"]
    extract --> transform
    transform --> load
```

## Data sample

![Data sample (book_df/master_books table)](./data-sample.png)
*Data sample (book_df/master_books table)*
