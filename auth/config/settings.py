# from decouple import config
from google.cloud import bigquery
import os
import google.auth
from google.oauth2 import service_account

from decouple import config

API_KEY=config("API_KEY")
LOGIN_URL = config("LOGIN_URL")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./auth/config/lexical-sol-361019-859206d82a0d.json"
credentials = service_account.Credentials.from_service_account_file(
    './auth/config/lexical-sol-361019-859206d82a0d.json' )

# credentials, project = google.auth.default(scopes=SCOPES)
credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/cloud-platform",
    ]
)



client = bigquery.Client(credentials=credentials, project=project)

def execute(query):
  # use yield to return data
  query_job = client.query(query)

  if query_job.result():
    return query_job.done(),query_job.result()





# scoped_credentials = credentials.with_scopes(
#     ['https://www.googleapis.com/auth/cloud-platform', SCOPES[0]])