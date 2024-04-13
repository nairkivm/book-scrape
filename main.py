import services.services as s

# Defining main function
def main():
    url = 'https://books.toscrape.com'
    raw_data = s.fetch_book_data(url)
    book_df = s.format_book_data(raw_data)
    s.load_book_data(book_df)

# Execute script
if __name__=="__main__":
    main()