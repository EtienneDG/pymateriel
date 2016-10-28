from bs4 import BeautifulSoup as bs
import requests


def get_page_content(url):
    try:
        return requests.get(url)
    except:
        return "Error :("


def get_soup(text):
    return bs.BeautifulSoup(text)

login_url = "https://www.materiel.net/pm/client/login.html"
html = get_page_content(login_url)
soup = get_soup(html)

loginInput = ""

