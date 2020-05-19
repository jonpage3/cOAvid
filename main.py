
#Version of online request searcher
#for general use; takes in user input

import requests, bs4,xlrd, re

from archives import red_shelf_searcher, pg_searcher, textbook_searcher, michigan_searcher, spread_sheet_searcher, \
    open_library_searcher, hathi_searcher, unc_searcher

s = requests.Session()

stopwords = ('a', 'able', 'all', 'also', 'am', 'an', 'and', 'any', 'are', 'as', 'ask', 'at', 'away',
             'b', 'be', 'been', 'best', 'both', 'but', 'by', 'c', 'came', 'can', 'cant', 'co', 'com', 'come',
             'd', 'did', 'do', 'does', 'done', 'down', 'e', 'each', 'edu', 'eg', 'else', 'et', 'etc', 'even', 'ever', 'ex',
             'f', 'far', 'few', 'five', 'for', 'four', 'from', 'g', 'get', 'gets', 'go', 'goes', 'gone', 'got',
             'h', 'had', 'has', 'have', 'he', 'help', 'her', 'here', 'hers', 'hi', 'him', 'his', 'how',
             'i', 'ie', 'if', 'in', 'inc', 'into', 'is', 'it', 'its', 'j', 'just', 'k', 'keep', 'kept', 'know',
             'l', 'last', 'less', 'lest', 'let', 'like', 'look', 'ltd', 'm', 'many', 'may', 'me', 'mean', 'more',
             'most', 'much', 'must', 'my', 'n', 'name', 'nd', 'near', 'need', 'new', 'next', 'nine', 'no', 'non', 'none',
             'nor', 'not', 'now', 'o', 'of', 'off', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto',
             'or', 'our', 'ours', 'out', 'over', 'own', 'p', 'per', 'plus', 'q', 'que', 'qv', 'r', 'rd', 're', 's', 'said',
             'same', 'saw', 'say', 'says', 'see', 'seem', 'seen', 'self', 'sent', 'she', 'six', 'so', 'some', 'soon', 'sub',
             'such', 'sup', 'sure', 't', 'take', 'tell', 'th', 'than', 'that', 'the', 'them', 'then', 'they', 'this', 'thru',
             'thus', 'to', 'too', 'took', 'try', 'two', 'u', 'un', 'unto', 'up', 'upon', 'us', 'use', 'used', 'uses',
             'uucp', 'v', 'very', 'via', 'viz', 'vs', 'w', 'want', 'was', 'way', 'we', 'well', 'went', 'were', 'what',
             'when', 'who', 'whom', 'why', 'will', 'wish', 'with', 'x', 'y', 'yes', 'yet', 'you', 'your', 'z', 'zero')

print("\t" + "\t" + "Welcome to the UNC online access searcher. Enter title/author or ISBN to search.")
print("\t" + "\t" + "\t" + "\t" + "(must include ISBN to search textbook database)")
print(" ")
print(" ")
print("LOADING FILES")
#Reading the static files that will be searched
jstor_cont = "y"
if jstor_cont == "y":
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
        input("Press enter to continue: ")
        jstor_cont = "n"

muse_cont = 'y'
if muse_cont == "y":
    print('Loading Project Muse database.')
    try:
        muse_workbook = xlrd.open_workbook("project_muse_free_covid_book.xlsx")
        muse_books = muse_workbook.sheet_by_index(0)
        museheadings = muse_books.row_values(0)
        musetitle_col = museheadings.index('Title')
        museauthor_col = museheadings.index('Contributor')
    except FileNotFoundError:
        print("Project Muse spreadsheet not found.")
        print("If file exists rename: project_muse_free_covid_book.xlsx, and restart program.")
        input("Press enter to continue: ")
        muse_cont = "n"

ohio_cont = 'y'
if ohio_cont == "y":
    print('Loading OSU Press database.')
    try:
        ohio_workbook = xlrd.open_workbook("OhioStateUnivPress-OpenTitles-KnowledgeBank.xlsx")
        ohio_books = ohio_workbook.sheet_by_index(0)
        ohioheadings = ohio_books.row_values(0)
        ohiotitle_col = ohioheadings.index('Title')
        ohioauthor_col = ohioheadings.index('Contributors')
    except FileNotFoundError:
        print("Ohio State Press open titles spreadsheet not found.")
        input("Press enter to continue: ")
        ohio_cont = 'n'

science_direct_cont = 'y'
if science_direct_cont == "y":
    print('Loading Science Direct database.')
    try:
        sd_workbook = xlrd.open_workbook("sciencedirect.xlsx")
        sd_books = sd_workbook.sheet_by_index(0)
        sdheadings = sd_books.row_values(0)
        sdtitle_col = sdheadings.index("publication_title")
        sdauthor_col = sdheadings.index("first_author")
    except FileNotFoundError:
        print("Science Direct items spreadsheet not found.")
        print("If file exists rename: sciencedirect.xlsx, and restart program.")
        input("Press enter to continue: ")
        science_direct_cont = 'n'

michigan_cont = 'y'
if michigan_cont == "y":
    print('Loading Michigan database.')
    fulcrum_searchtxt = ""
    regex = re.compile('[^a-zA-Z]')
    for n in range(1,13):
        fulcrum = s.get("https://www.fulcrum.org/michigan?locale=en&page={n}&per_page=1000&view=list".format(n=n))
        fulcrumSoup = bs4.BeautifulSoup(fulcrum.text,'html.parser')
        fulcrumSouptags = fulcrumSoup.select("#documents")
        fulcrumugly = fulcrumSouptags[0].getText()
        fulcrumtext = regex.sub('', fulcrumugly)
        fulcrumtext = fulcrumtext.lower()
        fulcrum_searchtxt = "".join([fulcrum_searchtxt,fulcrumtext])

vitalsource_cont = 'y'
if vitalsource_cont == "y":
    print('Loading textbook database.')
    try:
        textbook_workbook = xlrd.open_workbook('Spring 2020 Book List.xlsx')
        textbooks = textbook_workbook.sheet_by_index(0)
        tb_issn_col = 2
    except FileNotFoundError:
        print("Textbooks spreadsheet not found.")
        print("If file exists rename: Spring 2020 Book List.xlsx, and restart program.")
        input("Press enter to continue: ")
        vitalsource_cont = 'n'

gutenberg_cont = 'y'
if gutenberg_cont == 'y':
    print('Loading Gutenberg database.')
    try:
        fin = open('GUTINDEX.txt', encoding="utf-8")
    except FileNotFoundError:
        print("GUTINDEX.txt file not found.")
        input("Press enter to continue: ")
        gutenberg_cont = 'n'

#a couple helper functions
def return_helper(result,list):
    if result.__class__.__name__  == 'tuple':
        for item in result:
            print(item)
            list.append(item)
    elif result.__class__.__name__ == 'dict':
        for key in result:
            print(key)
            list.append(key)
            for elem in result[key]:
                print(elem)
                list.append(elem)
    else:
        print(result)
        list.append(result)


#helper for converting list to textfile
def list_to_file(var_list,name):
    file_name = name + '.txt'
    #open file for writing
    outfile = open(file_name, 'w',encoding='utf-8')
    #write the list to file
    for item in var_list:
        outfile.write(item + '\n')
    outfile.close()
    return file_name

print(" ")
cont = "y"
while cont == "y":
    request = []
    title_long = input("Enter title: ")
    title_split = title_long.split(':')
    title = title_split[0]
    author_num = input("Enter author: ")
    author = ""
    if len(author_num) > 0:
        for i in author_num:
            if i.isalpha() or i.isspace():
                author = "".join([author, i])
    if vitalsource_cont == "y":
        issn = input('Enter ISBN: ')

    print(title.upper())
    request.append(title.upper())
    print(author)
    request.append(author)

    unc_result = unc_searcher.searcher(title, author)
    return_helper(unc_result, request)

    hathi_temp_result = hathi_searcher.temp_access(title, author)
    return_helper(hathi_temp_result, request)
    hathi_full_time_result = hathi_searcher.full_time_access(title, author)
    return_helper(hathi_full_time_result, request)

    open_library_result = open_library_searcher.searcher(title, author)
    return_helper(open_library_result, request)

    red_shelf_result = red_shelf_searcher.searcher(title, author)
    return_helper(red_shelf_result, request)

    #spreadsheet searchers
    if jstor_cont == "y":
        return_helper(spread_sheet_searcher.searcher(title,author,jstor_books,jstortitle_col,jstorauthor_col,"JSTOR.","https://www.jstor.org/open/"),request)
    if muse_cont == "y":
        return_helper(spread_sheet_searcher.searcher(title,author,muse_books,musetitle_col,museauthor_col,"Project Muse.","https://muse.jhu.edu/search?action=oa_browse"),request)
    if ohio_cont == 'y':
        return_helper(spread_sheet_searcher.searcher(title,author,ohio_books,ohiotitle_col,ohioauthor_col,"Ohio State Uni Press.","https://kb.osu.edu/handle/1811/131"),request)
    if science_direct_cont == 'y':
        return_helper(spread_sheet_searcher.searcher(title,author,sd_books,sdtitle_col,sdauthor_col,"Science Direct Holdings.",
                                                     "https://auth.lib.unc.edu/ezproxy_auth.php?url=http://www.sciencedirect.com/science/books"),request)

    #michigan searcher
    if michigan_cont == "y":
        return_helper(michigan_searcher.searcher(title,author,fulcrum_searchtxt),request)

    #vital source searcher
    if vitalsource_cont == "y":
        return_helper(textbook_searcher.searcher(tb_issn_col,issn,title,textbooks),request)

    #gutenberg searcher
    if gutenberg_cont == "y":
        return_helper(pg_searcher.searcher(title,author,fin),request)

    print('----------------')
    request.append('----------------')
    list_to_file(request, title + "_" "results")

    print("Another search? (press y)  Enter any other button to exit.")
    cont = input("Enter: ")

