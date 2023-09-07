import requests
from bs4 import BeautifulSoup as bs
from DBConnect import DBConnect

def parse(url, db_access_object):
    html = requests.get(url)
    soup = bs(html.content, "html.parser")
    book_divs = soup.find_all(class_="product_pod")
    for div in book_divs:
        title = div.find("h3").a.get("title").replace("'", "''")
        link = div.find("h3").a.get("href")
        price = div.find(class_="price_color").text.strip()
        stock = div.find(class_="instock availability").text.strip()
        db_access_object.persist(title, link, price, stock)
    
    if (soup.find(class_="next")):
        nextpage = soup.find(class_="next").a.get("href")
        if ("catalogue" in nextpage):
            nexturl = "https://books.toscrape.com/" + nextpage
            parse(nexturl, db_access_object)
        elif ("page" in nextpage):
            nexturl = "https://books.toscrape.com/catalogue/" + nextpage
            parse(nexturl, db_access_object)