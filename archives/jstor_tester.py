import xlrd
from spread_sheet_searcher import searcher

print('Loading JSTOR database.')
try:
    jstor_workbook = xlrd.open_workbook('jstor_books.xlsx')
    jstor_books = jstor_workbook.sheet_by_index(0)
    jstorheadings = jstor_books.row_values(0)
    jstortitle_col = jstorheadings.index('Title')
    jstorauthor_col = jstorheadings.index('Authors')
except FileNotFoundError:
    print("jstor spreadsheet not found.")
    print("If file exists rename: jstor_books.xlsx, and restart program. ")

cont = "y"
while cont == "y":
    title = input("enter title: ")
    author = input("enter author: ")
    returns = searcher(title,author,jstor_books,jstortitle_col,jstorauthor_col,"JSTOR.", "https://www.jstor.org/open/")
    print(returns)
    cont = input("search again?: ")









