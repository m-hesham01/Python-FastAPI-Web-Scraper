import psycopg2

class DBConnect:
    def __init__(self):
        # initiating database connection
        self.DB_NAME = "puffin_books"
        self.DB_USER = "postgres"
        self.DB_PASS = "root"
        self.DB_HOST = "localhost"
        self.DB_PORT = "5432"
        self.conn = psycopg2.connect(database=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST, port=self.DB_PORT)
        
        # creating the table "books" in case it is not present in the database
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS books (title VARCHAR(255), link VARCHAR(255), price VARCHAR(15), stock VARCHAR(15));")
        self.conn.commit()
    
    # a function to insert rows to the database
    def persist(self, title, link, price, stock):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO books (title, link, price, stock) VALUES ('" + title + "', '" + link + "', '" + price + "', '" + stock + "');")
        self.conn.commit()