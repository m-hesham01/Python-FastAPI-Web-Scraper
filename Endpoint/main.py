from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import psycopg2

app = FastAPI()
# must mount the directory containing the bootstrap.css file to the uvicorn server, otherwise the css styles wont be visible
app.mount("/static", StaticFiles(directory="static"), name="static")

# initializing the database connection
conn = psycopg2.connect(
    dbname="puffin_books",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

# endpoint to display the database's books
@app.get("/", response_class=HTMLResponse)
async def get_books():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()

    # a loop to create an html table to display all books' information
    i = 1
    table = "<table class='table table-striped'><tr><th>#</th><th>Title</th><th>Link</th><th>Price</th><th>Stock</th></tr>"
    for book in books:
        table += f"<tr><td>{i}</td><td>{book[0]}</td><td><a href='{book[1]}'>{book[1]}</a></td><td>{book[2]}</td><td>{book[3]}</td></tr>"
        i += 1
    table += "</table>"
    
    # the html of the page to be displayed
    page = """
    <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>Puffin Test</title>
            <link href='/static/bootstrap.css' rel='stylesheet' type='text/css'/>
        </head>
        <body>
            <div class='container-lg m-2'>
            """ + table + """
            </div>
        </body>
    </html>
    """

    return page

# running the applicaton on uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")
