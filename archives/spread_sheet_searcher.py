#general speadsheet searcher

import re

#basic searcher for the different books with spreadsheets
def searcher(title,author,books,title_col,author_col,db_name, return_url):
    title = title.lower()
    author = author.lower()
    regex = re.compile('[^a-zA-Z]')
    title = regex.sub('', title)
    author = regex.sub('', author)
    acc = 0
    for row in range(1, books.nrows):
        # string cleanup for each
        book_title = books.cell_value(row, title_col)
        book_title = regex.sub('', book_title)
        book_title = book_title.lower()
        author_title = books.cell_value(row, author_col)
        author_title = regex.sub('', author_title)
        author_title = author_title.lower()
        if title in book_title and author in author_title:
            acc += 1
    if acc > 0:

        return "Found in "+ db_name, return_url
    else:
        return "Not found in "+ db_name

