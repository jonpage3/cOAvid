
#searching michigan fulcrum project
import re, requests,bs4
s = requests.Session()

def searcher(title,author,searchtext):
    regex = re.compile('[^a-zA-Z]')
    title_search = regex.sub('',title)
    title_search = title_search.lower()
    author_search = regex.sub('',author)
    author_search = author_search.lower()
    if title_search in searchtext and author_search in searchtext:
        title = title.replace(" ", "+")
        return_url = "https://www.fulcrum.org/michigan?utf8=%E2%9C%93&press=michigan&q=%s" % title
        return "Found in Michigan Press Open Access.",return_url
    else:
        return "Not found in Michigan Press Open Access."

if __name__ == "__main__":

    print('Loading Michigan database.')
    fulcrum_searchtxt = ""
    regex = re.compile('[^a-zA-Z]')
    for n in range(1, 13):
        fulcrum = s.get("https://www.fulcrum.org/michigan?locale=en&page={n}&per_page=1000&view=list".format(n=n))
        fulcrumSoup = bs4.BeautifulSoup(fulcrum.text, 'html.parser')
        fulcrumSouptags = fulcrumSoup.select("#documents")
        fulcrumugly = fulcrumSouptags[0].getText()
        fulcrumtext = regex.sub('', fulcrumugly)
        fulcrumtext = fulcrumtext.lower()
        fulcrum_searchtxt = "".join([fulcrum_searchtxt, fulcrumtext])
    cont = "y"
    while cont == "y":
        title = input("enter title: ")
        author = input("enter author: ")
        returns = searcher(title, author)
        print(returns)
        cont = input("search again?: ")



