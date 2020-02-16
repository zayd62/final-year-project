from bs4 import BeautifulSoup as bs


def parse(content):
    """
    takes the table and returns the table as a dictionary
    """
    soup = bs(content, "html.parser")
    table = soup.find("table", class_="prodtable")
    rows = table.find_all("tr")
    table_lst = []
    for i, j in enumerate(rows):
        for k, l in enumerate(j):
            table_lst.append(l.text)

    dct = {}
    for m in range(0, len(table_lst), 2):
        dct[table_lst[m].strip(":")] = table_lst[m + 1]
    return dct
