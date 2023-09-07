from my_functions import parse
from DBConnect import DBConnect

# creating a single database access object that will be used throughout script's runtime
db_access_object = DBConnect()

url = "https://books.toscrape.com/"

parse(url, db_access_object)