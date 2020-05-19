
from flask import (Flask, Response, request, render_template, make_response,
                   redirect)
from flask_restful import Api, Resource, reqparse, abort

from archives import red_shelf_searcher, pg_searcher, textbook_searcher, michigan_searcher, spread_sheet_searcher, \
    open_library_searcher, hathi_searcher, unc_searcher

import webbrowser

app = Flask(__name__)
api = Api(app)

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
