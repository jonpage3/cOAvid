#open_library searcher
import requests, bs4
s = requests.Session()
#open libray function
def searcher(title,author):
    title_open = title.replace(" ", "+")
    author_no_end_space = author.strip(" ")
    author_open = author_no_end_space.replace(" ", "+")
    open_lib_url = 'https://openlibrary.org/search?title=%s&author=%s' %(title_open, author_open)
    open_lib = s.get(open_lib_url)
    openSoup = bs4.BeautifulSoup(open_lib.text,'html.parser')
    if 'No results found.' in open_lib.text:
        return 'Not found in Open Library.'

    else:
        open_items_elem = openSoup.select('.searchResultItemCTA-lending')
        acc = 0
        for x in range(len(open_items_elem)):
            if 'Not in Library' in open_items_elem[x].getText():
                continue
            else:
                acc +=1
        if acc > 0:
            #print(title)
            #print(author)
            return 'Found in Open Library.',open_lib_url

        else:
            return 'Not found in Open Library.'

if __name__ == "__main__":

    cont = "y"
    while cont == "y":
        title = input("enter title: ")
        author = input("enter author: ")
        returns = searcher(title,author)
        print(returns)
        cont = input("search again?: ")