#red_shelf_access
import requests, bs4
s = requests.Session()

stopwords = ('a', 'able', 'all', 'also', 'am', 'an', 'and', 'any', 'are', 'as', 'ask', 'at', 'away',
                 'b', 'be', 'been', 'best', 'both', 'but', 'by', 'c', 'came', 'can', 'cant', 'co', 'com', 'come',
                 'd', 'did', 'do', 'does', 'done', 'down', 'e', 'each', 'edu', 'eg', 'else', 'et', 'etc', 'even',
                 'ever', 'ex',
                 'f', 'far', 'few', 'five', 'for', 'four', 'from', 'g', 'get', 'gets', 'go', 'goes', 'gone', 'got',
                 'h', 'had', 'has', 'have', 'he', 'help', 'her', 'here', 'hers', 'hi', 'him', 'his', 'how',
                 'i', 'ie', 'if', 'in', 'inc', 'into', 'is', 'it', 'its', 'j', 'just', 'k', 'keep', 'kept', 'know',
                 'l', 'last', 'less', 'lest', 'let', 'like', 'look', 'ltd', 'm', 'many', 'may', 'me', 'mean', 'more',
                 'most', 'much', 'must', 'my', 'n', 'name', 'nd', 'near', 'need', 'new', 'next', 'nine', 'no', 'non',
                 'none',
                 'nor', 'not', 'now', 'o', 'of', 'off', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only',
                 'onto',
                 'or', 'our', 'ours', 'out', 'over', 'own', 'p', 'per', 'plus', 'q', 'que', 'qv', 'r', 'rd', 're', 's',
                 'said',
                 'same', 'saw', 'say', 'says', 'see', 'seem', 'seen', 'self', 'sent', 'she', 'six', 'so', 'some',
                 'soon', 'sub',
                 'such', 'sup', 'sure', 't', 'take', 'tell', 'th', 'than', 'that', 'the', 'them', 'then', 'they',
                 'this', 'thru',
                 'thus', 'to', 'too', 'took', 'try', 'two', 'u', 'un', 'unto', 'up', 'upon', 'us', 'use', 'used',
                 'uses',
                 'uucp', 'v', 'very', 'via', 'viz', 'vs', 'w', 'want', 'was', 'way', 'we', 'well', 'went', 'were',
                 'what',
                 'when', 'who', 'whom', 'why', 'will', 'wish', 'with', 'x', 'y', 'yes', 'yet', 'you', 'your', 'z',
                 'zero')

def searcher(title,author):
    title = title.lower()
    author = author.lower()
    query = title + " " + author
    red_query = query.replace(" ", "+")
    red_shelf_url = 'https://studentresponse.redshelf.com/search/?terms=%s' % red_query
    red_shelf = s.get(red_shelf_url)

    redSoup = bs4.BeautifulSoup(red_shelf.text, 'html.parser')
    red_items = redSoup.select(".price-content")
    if len(red_items) > 0:
        if "Borrow through" in red_items[0].getText():
            title_items = redSoup.select(".title-row")
            # print(title_items[0].getText())
            t1 = title_items[0].getText()
            t1 = t1.lower()
            t1_list = t1.split()
            t1_no_stop = [word for word in t1_list if not word in stopwords]

            t2 = "".join(t1_no_stop)

            #remove stopwords from title
            title_list = title.split()
            title_no_stop = [word for word in title_list if not word in stopwords]
            title_nospace = "".join(title_no_stop)

            if title_nospace in t2:

                return "Found in Red Shelf.", red_shelf_url
            else:
                return "Not found in Red Shelf."
        else:
            return "Not found in Red Shelf"
    else:
        return "Not found in Red Shelf"

if __name__ == "__main__":

    cont = "y"
    while cont == "y":
        title = input("enter title: ")
        author = input("enter author: ")
        returns = searcher(title,author)
        print(returns)
        cont = input("search again?: ")



