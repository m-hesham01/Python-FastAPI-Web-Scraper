import requests
from bs4 import BeautifulSoup as bs
from DBConnect import DBConnect

# a recursive function that terminates only when there are no more "next" pages to load
def parse(url, db_access_object):
    # loading the page's html
    html = requests.get(url)
    soup = bs(html.content, "html.parser")
    
    # extracting the relevant information and writing it to the database
    book_divs = soup.find_all(class_="product_pod")
    for div in book_divs:
        
        # apostrophes found in book titles cause the query to fail, so this is in order to fix it
        title = div.find("h3").a.get("title").replace("'", "''")
        link = div.find("h3").a.get("href")
        price = div.find(class_="price_color").text.strip()
        stock = div.find(class_="instock availability").text.strip()
        db_access_object.persist(title, link, price, stock)
    
    # checking if there is a "next button on the current page"
    if (soup.find(class_="next")):
        nextpage = soup.find(class_="next").a.get("href")
        
        #only page 2 contains "catalogue/" in its url, but pages 3-50 do not
        if ("catalogue" in nextpage):
            nexturl = "https://books.toscrape.com/" + nextpage
            # calling parse function to the next page
            parse(nexturl, db_access_object)
        elif ("page" in nextpage):
            nexturl = "https://books.toscrape.com/catalogue/" + nextpage
            # calling parse function to the next page
            parse(nexturl, db_access_object)