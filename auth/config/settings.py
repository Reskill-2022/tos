# from decouple import config
from google.cloud import bigquery
import os
import json
from decouple import config

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./auth/config/lexical-sol-361019-5ab9cc34711e.json"

client = bigquery.Client()

def execute(query):
  # use yield to return data
  query_job = client.query(query)

  if query_job.result():
    yield query_job.done(),query_job.result()
