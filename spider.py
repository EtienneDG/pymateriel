import bs4
import requests
import csv
import datetime

# credentials
login = ""
password = ""


def connect(s, l, p):
    login_url = "https://www.materiel.net/pm/client/logincheck.nt.html"
    login_data = {"login": l, "pass": p}
    return s.post(login_url, data=login_data)


def soup_get_deepest_child(soup_element):
    list_children = [c for c in list(soup_element.children) if type(c) == bs4.element.Tag]
    if len(list_children) == 0:
        return str(soup_element.contents[0])
    else:
        return soup_get_deepest_child(list_children[0])


def table_to_csv(soup_table):
    run_date = str(datetime.datetime.now().replace(microsecond=0))
    for row in soup_table.find("tbody").find_all("tr"):
        cells = row.find_all("td", recursive=False)
        product = soup_get_deepest_child(cells[0])
        price = soup_get_deepest_child(cells[2])
        availability = str(True if soup_get_deepest_child(cells[3]) == "EN STOCK" else False)
        print(product + " " + price + " " + availability)
        with open("shopping_list.csv", "a+", newline="\n") as csv_file:
            csv_writer = csv.writer(csv_file, dialect="unix")
            csv_writer.writerow([run_date,  product, price, availability])

# MAIN
current_session = requests.Session()

if connect(current_session, login, password).status_code == 200:
    r = current_session.get("https://www.materiel.net/pm/client/shopping.html")
else:
    exit("failed to connect =(")

soup = bs4.BeautifulSoup(r.content, "html.parser")
shopping_list = soup.find("table", {"class": "BskProdList"})
table_to_csv(shopping_list)
