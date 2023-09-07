FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY main.py .
COPY /static/bootstrap.css ./static/
EXPOSE 80
CMD ["bash", "-c", "python -m uvicorn main:app --port=80 --reload"]