#UNC catalog function
import requests, bs4, re
s = requests.Session()
def searcher(title,author):
    # helper string
    oncheck = "onlinefulltextavailable"
    #compile regular expression
    regex = re.compile('[^a-zA-Z]')
    #string editing to make query
    title = title.lower()
    title = title.replace(" ", "+")
    author = author.lower()
    author = author.replace(" ", "+")
    #query for unc url
    query = title + "+" + author
    unc_url = "https://catalog.lib.unc.edu/?utf8=%E2%9C%93&search_field=all_fields&q={query}&f%5Baccess_type_f%5D%5B%5D=Online".format(
        query=query)
    unc_get = s.get(unc_url)
    #create bsoup object
    uncSoup = bs4.BeautifulSoup(unc_get.text, 'html.parser')
    #this is one way to select the items on the UNC page
    #using schema.org/Thing seemed like the best way
    unc_items = uncSoup.find_all("div", {"itemtype": "http://schema.org/Thing"})

    title = regex.sub('', title)
    author = regex.sub('', author)
    #dictionary in case multiple links
    found_dic = {"Found at UNC: ": []}
    unc_acc = 0
    for item in unc_items:
        search_soup = item.getText()
        search_clean = regex.sub('', search_soup)
        search_clean = search_clean.lower()
        if title in search_clean and author in search_clean and oncheck in search_clean:
            #for each item find all links
            link_elems = item.find_all("a")
            link_urls = [x.get("href") for x in link_elems]
            for url in link_urls:
                if url.startswith('/'):
                    url = "https://catalog.lib.unc.edu" + url
                found_dic["Found at UNC: "].append(url)
            unc_acc +=1

    if unc_acc > 0:
        return found_dic
    else:
        return "Not found in UNC catalog."

if __name__ == "__main__":

    cont = "y"
    while cont == "y":
        title = input("enter title: ")
        author = input("enter author: ")
        returns = searcher(title,author)
        print(returns)
        cont = input("search again?: ")