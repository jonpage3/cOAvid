#gutenberg searcher
#currently using database GUTINDEX.txt
import re
def searcher(title_input,author_input,file):
    regex = re.compile('[^a-zA-Z]')
    title = regex.sub('', title_input)
    author = regex.sub('', author_input)
    title = title.lower()
    author = author.lower()
    acc = 0
    for line in file:
        line = line.lower()
        line = regex.sub('',line)
        if title in line and author in line:
            acc +=1

    if acc > 0:
        query = title_input + ' ' + author_input
        query = query.replace(' ', '+')
        gutenberg_url = "http://www.gutenberg.org/ebooks/search/?query=%s" % query
        return "Found at Project Gutenberg.", gutenberg_url
    else:
        return "Not found at Project Gutenberg."

if __name__ == "__main__":

    print('Loading Gutenberg database.')
    try:
        fin = open('GUTINDEX.txt', encoding="utf-8")
        cont = "y"
        while cont == "y":
            title = input("enter title: ")
            author = input("enter author: ")
            returns = searcher(title, author, fin)
            print(returns)
            cont = input("search again?: ")
    except FileNotFoundError:
        print("GUTINDEX.txt file not found.")
        input("Press enter to continue: ")

