from fastapi import  APIRouter, HTTPException
from auth.schemas.tos_schema import TOS
from auth.config.settings import execute, API_KEY, LOGIN_URL
import requests



app = APIRouter()

table_name="`lexical-sol-361019.2022_survey_export.intro_phase_scheduled_fetch`"
table_name = "`lexical-sol-361019.2022_survey_export.intro_phase`"

@app.post("/tos/terms-of-service")
async def read_root(data:TOS,):
  """

  This endpoint is used to store user email after they accept terms of service
    then set a cookie to the user browser to prevent them from seeing the terms of service again

  Args:

      - email: [This is the email of the user. It is a required string field]
      - tos_accpted: [This is the terms of service accepted by the user. It is a required boolean value]
  """

  # check if all fields are filled
  if data.email == "" and data.tos_accepted != True:
    raise HTTPException(status_code=400, detail="Please fill all fields")

  # check if email exists
  email_checker = list(execute( f"SELECT * FROM `lexical-sol-361019.2022_tos_export.tos` WHERE email = '{data.email}'"))

  # get email count from email_checker
  email = [email["email"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0 :
    return "You have already accepted the terms of service"

  # insert data
  try:
    tos_write = execute(f"INSERT INTO \
            `lexical-sol-361019.2022_tos_export.tos` \
            (email, tos_accepted, created_at, updated_at) \
            VALUES ('{data.email}', \
            {data.tos_accepted}, \
            '{data.created_at}', \
            '{data.updated_at}')")
    
    return {"message": "Success", 
            "data": tos_write, 
    }

  except Exception as e:
    raise HTTPException(status_code=400, detail={"message": "Something went wrong", "data":e})


# endpoint to check if user email exists
@app.get("/tos/okta/{email}")
async def read_root(email:str):
  """

  This endpoint is used to check if user email exists

  Args:

      - email: [This is the email of the user. It is a required string field]
  """

  is_oktam_mail =await get_user(email)


  if is_oktam_mail:
        return {"is_otka_mail": True, "message": "Email exists"}

  raise HTTPException(404, {"Okta_email": False, "message": "Okta does not recognise you by this mail. Kindily fill the form again with the email address you use in signing into okta."})


@app.get("/tos/survey/{email}")
async def read_suvey_mai(email:str):
  """

  This endpoint is used to check if user email exists

  Args:

      - email: [This is the email of the user. It is a required string field]
  """

  # check if email exists
  email_checker = list(execute( f"SELECT * FROM {table_name} WHERE email_address = '{email}'"))

  # get email count from email_checker
  email = [email["email_address"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0:
    return {"is_survey_filled": True, "message": "Email exists"}
  
  raise HTTPException(404, {"survey_filled": False, "message": "We do not recognise by this email address. Kindily fill the form again with the email address you use in signing into okta."})



# check if user email exists in okta
async def get_user(email):

  url = f"{LOGIN_URL}/api/v1/users?q={email}&limit=1"

  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"SSWS {API_KEY}"
  }

  response = requests.request("GET", url, headers=headers)

  if response.json() == []:
    return False

  return True


