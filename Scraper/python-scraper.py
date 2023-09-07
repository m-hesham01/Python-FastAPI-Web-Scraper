from my_functions import parse
from DBConnect import DBConnect

print("code is running")

db_access_object = DBConnect()
url = "https://books.toscrape.com/"
parse(url, db_access_object)