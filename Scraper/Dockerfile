FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY DBConnect.py .
COPY my_functions.py .
COPY python-scraper.py .
EXPOSE 5000
CMD ["bash", "-c", "python python-scraper.py"]
