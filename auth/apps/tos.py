from fastapi import  APIRouter, HTTPException
from auth.schemas.tos_schema import TOS
from auth.config.settings import execute


app = APIRouter()


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
@app.get("/tos/survey/{email}")
async def read_root(email:str):
  """

  This endpoint is used to check if user email exists

  Args:

      - email: [This is the email of the user. It is a required string field]
  """

  # check if email exists
  email_checker = list(execute( f"SELECT * FROM `lexical-sol-361019.2022_survey_export.intro_phase` WHERE email = '{email}'"))

  # get email count from email_checker
  email = [email["email"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0 :
    return {"bool": True, "message": "Email exists"}

  return {"bool": False, "message": "Email does not exist"}