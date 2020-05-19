
from flask import (Flask, Response, request, render_template, make_response,
                   redirect)
from flask_restful import Api, Resource, reqparse, abort

from archives import red_shelf_searcher, pg_searcher, textbook_searcher, michigan_searcher, spread_sheet_searcher, \
    open_library_searcher, hathi_searcher, unc_searcher

import xlrd,webbrowser,re,requests,bs4


s = requests.Session()
print("\t" + "\t" + "Welcome to cOAvid (carolina open access virtual item determiner/digger/detective)")

print(" ")
print(" ")
print("LOADING FILES")
##############################
# import static databases    #
##############################
print('Loading JSTOR database.')
try:
    jstor_workbook = xlrd.open_workbook('jstor_books.xlsx')
    jstor_books = jstor_workbook.sheet_by_index(0)
    jstorheadings = jstor_books.row_values(0)
    jstortitle_col = jstorheadings.index('Title')
    jstorauthor_col = jstorheadings.index('Authors')
    jstor_cont = "y"
except FileNotFoundError:
    print("jstor spreadsheet not found.")
    print("If file exists rename: jstor_books.xlsx, and restart program. ")
    jstor_cont = "n"

print('Loading Project Muse database.')
try:
    muse_workbook = xlrd.open_workbook("project_muse_free_covid_book.xlsx")
    muse_books = muse_workbook.sheet_by_index(0)
    museheadings = muse_books.row_values(0)
    musetitle_col = museheadings.index('Title')
    museauthor_col = museheadings.index('Contributor')
    muse_cont = "y"
except FileNotFoundError:
    print("Project Muse spreadsheet not found.")
    print("If file exists rename: project_muse_free_covid_book.xlsx, and restart program.")
    muse_cont = "n"

print('Loading OSU Press database.')
try:
    ohio_workbook = xlrd.open_workbook("OhioStateUnivPress-OpenTitles-KnowledgeBank.xlsx")
    ohio_books = ohio_workbook.sheet_by_index(0)
    ohioheadings = ohio_books.row_values(0)
    ohiotitle_col = ohioheadings.index('Title')
    ohioauthor_col = ohioheadings.index('Contributors')
    ohio_cont = 'y'
except FileNotFoundError:
    print("Ohio State Press open titles spreadsheet not found.")
    ohio_cont = 'n'

print('Loading Science Direct database.')
try:
    sd_workbook = xlrd.open_workbook("sciencedirect.xlsx")
    sd_books = sd_workbook.sheet_by_index(0)
    sdheadings = sd_books.row_values(0)
    sdtitle_col = sdheadings.index("publication_title")
    sdauthor_col = sdheadings.index("first_author")
    science_direct_cont = "y"
except FileNotFoundError:
    print("Science Direct items spreadsheet not found.")
    print("If file exists rename: sciencedirect.xlsx, and restart program.")
    input("Press enter to continue: ")
    science_direct_cont = 'n'

print('Loading Michigan database.')
michigan_cont = 'y'
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

print('Loading textbook database.')
try:
    textbook_workbook = xlrd.open_workbook('Spring 2020 Book List.xlsx')
    textbooks = textbook_workbook.sheet_by_index(0)
    tb_issn_col = 2
    vitalsource_cont = 'y'
except FileNotFoundError:
    print("Textbooks spreadsheet not found.")
    print("If file exists rename: Spring 2020 Book List.xlsx, and restart program.")
    vitalsource_cont = 'n'

print('Loading Gutenberg database.')
try:
    fin = open('GUTINDEX.txt', encoding="utf-8")
    gutenberg_cont = 'y'
except FileNotFoundError:
    print("GUTINDEX.txt file not found.")
    gutenberg_cont = 'n'

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

## Specify the data necessary to create a new search
#
new_request_parser = reqparse.RequestParser()
for arg in ['title','author','isbn']:
    new_request_parser.add_argument(
        arg, required=False)


#a couple helper functions
def return_helper(result,list):
    if result.__class__.__name__  == 'tuple':
        for item in result:
            list.append(item)
    elif result.__class__.__name__ == 'dict':
        for key in result:
            list.append(key)
            for elem in result[key]:
                list.append(elem)
    else:
        list.append(result)



# home page of search
class Search(Resource):

    def get(self):

        return make_response(render_template('search.html'),'200')


class Search_results(Resource):

    def get(self):
        request = new_request_parser.parse_args()
        results = []
        title = request['title']
        author = request['author']
        isbn = request['isbn']

        unc_result = unc_searcher.searcher(title, author)
        return_helper(unc_result, results)

        hathi_temp_result = hathi_searcher.temp_access(title, author)
        return_helper(hathi_temp_result, results)
        hathi_full_time_result = hathi_searcher.full_time_access(title, author)
        return_helper(hathi_full_time_result, results)

        open_library_result = open_library_searcher.searcher(title, author)
        return_helper(open_library_result, results)

        red_shelf_result = red_shelf_searcher.searcher(title, author)
        return_helper(red_shelf_result, results)
        # spreadsheet searchers
        if jstor_cont == "y":
            return_helper(
                spread_sheet_searcher.searcher(title, author, jstor_books, jstortitle_col, jstorauthor_col, "JSTOR.","https://www.jstor.org/open/"),
                results)
        if muse_cont == "y":
            return_helper(spread_sheet_searcher.searcher(title, author, muse_books, musetitle_col, museauthor_col,
                                                         "Project Muse.",
                                                         "https://muse.jhu.edu/search?action=oa_browse"), results)
        if ohio_cont == 'y':
            return_helper(spread_sheet_searcher.searcher(title, author, ohio_books, ohiotitle_col, ohioauthor_col,
                                                         "Ohio State Uni Press.", "https://kb.osu.edu/handle/1811/131"),
                          results)
        if science_direct_cont == 'y':
            return_helper(spread_sheet_searcher.searcher(title, author, sd_books, sdtitle_col, sdauthor_col,
                                                         "Science Direct Holdings.",
                                                         "https://auth.lib.unc.edu/ezproxy_auth.php?url=http://www.sciencedirect.com/science/books"),
                          results)
        if michigan_cont == "y":
            return_helper(michigan_searcher.searcher(title, author, fulcrum_searchtxt), results)

        if vitalsource_cont == "y":
            return_helper(textbook_searcher.searcher(tb_issn_col, isbn, title, textbooks), results)

        if gutenberg_cont == "y":
            return_helper(pg_searcher.searcher(title, author, fin), results)

        #pull the links out of results list
        links = [result for result in results if "http" in result]

        if len(links) > 0:
            return make_response(render_template('search_results.html', request=request, links=links,result=""), '200')
        else:
            return make_response(render_template('search_results.html', request=request, links=links,result="No results were found."), '200')




app = Flask(__name__)
api = Api(app)
api.add_resource(Search,'/search')
api.add_resource(Search_results,'/search_results')

@app.route('/')
def index():
    return redirect(api.url_for(Search), code=303)

if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000/")
    app.run()
