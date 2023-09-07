# Python-FastAPI-Web-Scraper
### Scraping Book Title, Price, Stock Availability and URLs for Books on https://books.toscrape.com/



## Instructions to run scraper locally:

1- Create the database locally using the command 
  `CREATE DATABASE puffin_books;`
  in PSQL shell

2- Check **Scraper/DBConnect.py** for database credentials and edit them if necessary

3- Run 
  
  `pip install requests`

  `pip install beautifulsoup4`
  
  `pip install psycopg2`
  
  if the modules are not existent on your local machine

4- Finally, when everything is set up, run the **Scraper/python-scraper.py** code using `python Scraper/python-scraper.py` or by using an IDE such as Visual Studio Code

5- Validate that entries have been inserted into the database by running `SELECT COUNT (*) FROM books;` in PSQL shell. This query should return 1000, which is the number of books on the website

![image](https://github.com/m-hesham01/Python-FastAPI-Web-Scraper/assets/93948325/0e4aa0f7-abdf-4ab4-80c8-185212bdbce7)


## Instructions to run endpoint locally:

1- Check **Endpoint/main.py** for database credentials and edit them if necessary

2- Run 
  
  `pip install fastapi`

  `pip install requests`
  
  if the modules are not existent on your local machine
  
3- Run the application by heading to the **Endpoint** directory and executing

`python -m uvicorn main:app --reload`


4- If application startup is complete, head to the given IP Address (Possibly **http://127.0.0.1:8000**) and the page should load as such:

![image](https://github.com/m-hesham01/Python-FastAPI-Web-Scraper/assets/93948325/8bf146f6-fc88-4b98-a219-cfa81945b80a)

##############################################################################################
##############################################################################################
##############################################################################################

## Instructions to run scraper on cloud:
### I have set up a Kubernetes Cluster on Microsoft Azure so the next steps will apply to that
### For help setting up your Microsoft Azure Kubernetes Cluster visit this page: https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster

1- Prep your environment by executing the following commands in CMD:

`az login`

`az aks get-credentials --resource-group <your-resource-group> --name <your-aks-cluster>`

2- Set up PostgreSQL via the following steps:
  - Create a Persisten Volume Claim by applying **Scraper/yaml/postgres-pvc.yaml** in CMD `kubectl apply -f postgres-pvc.yaml`
  - Create a Persisten Volume by applying **Scraper/yaml/postgres-pv.yaml** in CMD `kubectl apply -f postgres-pv.yaml`
  - Create a Postgres Deployment by applying **Scraper/yaml/postgres-deployment.yaml** in CMD `kubectl apply -f postgres-deployment.yaml`
  - Finally, create a service to expose your Postgres deployment to other deployments on the cluster by applying **Scraper/yaml/postgres-service.yaml** in CMD `kubectl apply -f postgres-service.yaml`

3- Create the database:
  - Get the deployment name by executing the command `kubectl get pods`
    ![image](https://github.com/m-hesham01/Python-FastAPI-Web-Scraper/assets/93948325/299ef0f6-6ab1-4369-9185-fdc216e31f89)
    
  - Run the command `kubectl exec -it <postgres-pod-name> -- psql -U postgres` to start an interactive PSQL shell session inside of the postgres pod
  - Within the pod's interactive shell, run `CREATE DATABASE puffin_books;` then exit after database is successfully created by executing `\q`

4- Deploy scraper:
  - Apply **Scraper/yaml/python-scraper-job.yaml** in CMD `kubectl apply -f python-scraper-job.yaml`
    
5- Validate that entries have been inserted into the database
  - Run the command `kubectl exec -it <postgres-pod-name> -- psql -U postgres`
  - Within the pod's interactive shell, switch to the correct database by executing `\c puffin_books`
  - And once again, run `SELECT COUNT (*) FROM books;`

## Instructions to run endpoint on cloud:

1- Deploy FastAPI endpoint:
  - Apply **Endpoint/yaml/fastapi-app.yaml** in CMD `kubectl apply -f fastapi-app.yaml`
  - Execute `kubectl get pods` to find FastAPI app
    ![image](https://github.com/m-hesham01/Python-FastAPI-Web-Scraper/assets/93948325/3457ea26-d079-47e9-8352-ab654ed8c343)
  - Step into the deployment's container by executing `kubectl exec -it <fastapi-app-pod-name> /bin/bash`
  - Run `curl 127.0.0.1:80` which should return all of the HTML for the table on the webpage (it's a lot, so feel free to `clear` afterwards)
    
2- Expose an external IP Address to access the deployment:
  - Apply **Endpoint/yaml/fastapi-service.yaml** in CMD `kubectl apply -f fastapi-service.yaml`
  - Execute `kubectl get services` to find FastAPI LoadBalancer's External IP Address and Port
    ![image](https://github.com/m-hesham01/Python-FastAPI-Web-Scraper/assets/93948325/b28884e9-c21e-4b4e-a208-73e23e040d86)
  - Navigate to the given IP Address in your local browser

