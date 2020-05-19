#right now only searching ISSNs
#textbook searcher
import xlrd
def searcher(tb_issn_col,issn,title,textbooks):
    if issn == "":
        return "Not found in Students Stores textbook spreadsheet."
    else:
        for row in range(1,textbooks.nrows):
            if issn == str(textbooks.cell_value(row,tb_issn_col)):
                vital_query = title.replace(" ", "%20")
                vital_url = "https://bookshelf.vitalsource.com/#/search?q=%s" % vital_query
                return "Found in Textbooks. Could be available here:", vital_url
            else:
                return "Not found in Students Stores textbook spreadsheet."

if __name__ == "__main__":

    print('Loading textbook database.')
    try:
        textbook_workbook = xlrd.open_workbook('Spring 2020 Book List.xlsx')
        textbooks = textbook_workbook.sheet_by_index(0)
        tb_issn_col = 2
        cont = "y"
        while cont == "y":
            title = input("enter title")
            issn = input("enter isbn")
            returns = searcher(tb_issn_col,issn,title)
            print(returns)
            cont = input("search again?: ")
    except FileNotFoundError:
        print("Textbooks spreadsheet not found.")
        print("If file exists rename: Spring 2020 Book List.xlsx, and restart program.")
        input("Press enter to continue: ")


