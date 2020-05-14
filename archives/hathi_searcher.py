import requests, bs4, re
s = requests.Session()

# search actual hathitrust site for always accessible
def full_time_access(title,author):
    title = title.lower()
    author = author.lower()
    author = author.strip(" ")
    title_query = title.replace(" ","+")
    author_query = author.replace(" ","+")
    query = title_query + "+" + author_query
    ht_url = "https://catalog.hathitrust.org/Search/Home?lookfor={query}&ft=ft&setft=true".format(
        query=query)
    ht_page = s.get(ht_url)
    htSoup = bs4.BeautifulSoup(ht_page.text, 'html.parser')
    records = htSoup.select('.record')

    if len(records) > 0:
        hathi_acc = 0
        # get text for each record
        records_list = [x.getText() for x in records]
        # cleanup using regular expressions
        regex = re.compile('[^a-zA-Z]')
        record_clean_list = []
        for record in records_list:
            record_clean = regex.sub('', record)
            record_clean = record_clean.lower()
            record_clean_list.append(record_clean)
        # clean our search terms
        title_caps = regex.sub('', title)
        title_test = title_caps.lower()
        author_caps = regex.sub('', author)
        author_test = author_caps.lower()

        for record in record_clean_list:
            if title_test in record and author_test in record:
                hathi_acc += 1
        if hathi_acc > 0:
            return "Found in HathiTrust fulltime access.", ht_url
        else:
            return "Not found in HathiTrust fulltime access."

    else:
        return "Not found in HathiTrust fulltime access."

#hathi temp access searcher
def temp_access(title, author):
    title = title.lower()
    author = author.lower()
    title_unc = title.replace(" ", "+")
    author_no_end_space = author.strip(" ")
    author_unc = author_no_end_space.replace(" ", "+")
    query = author_unc + "+" + title_unc
    hathi_url = "https://catalog.lib.unc.edu/?utf8=%E2%9C%93&search_field=all_fields&q={query}&f%5Baccess_type_f%5D%5B%5D=Online".format(
        query=query)
    hathi_get = s.get(hathi_url)
    hathiSoup = bs4.BeautifulSoup(hathi_get.text, 'html.parser')
    hathi_items = hathiSoup.find_all("div", {"itemtype": "http://schema.org/Thing"})

    regex = re.compile('[^a-zA-Z]')
    title = regex.sub('', title)
    author = regex.sub('', author)
    #string for checking
    oncheck = "temporarilyavailable"
    hathi_dic = {"Temporary access: ": []}
    hathi_acc = 0
    for item in hathi_items:
        search_soup = item.getText()
        search_clean = regex.sub('', search_soup)
        search_clean = search_clean.lower()
        if title in search_clean and author in search_clean and oncheck in search_clean:
            bib_num = item.get("data-document-id")
            hathi_url = "https://catalog.lib.unc.edu/catalog/" + bib_num
            hathi_dic["Temporary access: "].append(hathi_url)
            hathi_acc +=1

    if hathi_acc > 0:
         return hathi_dic
    else:
         return "Not found in HathiTemp Access"


if __name__ == "__main__":

    cont = "y"
    while cont == "y":
        title = input("enter title: ")
        author = input("enter author: ")
        returns = full_time_access(title,author)
        print(returns)
        tempreturns = temp_access(title,author)
        print(tempreturns)
        cont = input("search again?: ")
