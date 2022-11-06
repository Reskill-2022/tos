from fastapi import APIRouter
from auth.config.settings import execute
from auth.schemas.survey_schema import Survey
from fastapi import  APIRouter, HTTPException, Request
from starlette.responses import Response

app = APIRouter()


# survey endpoint
@app.post("/survey")
async def read_root(data:Survey, response:Response):

  #  verify if all fields in survey_schema are filled
  if data.email == "" or data.data == "":
    raise HTTPException(status_code=400, detail="Please fill all fields")
  
  # check if email exists
  email_checker = list(execute( f"SELECT * FROM `lexical-sol-361019.RA_TOS_SURVEY.survey` WHERE email = '{data.email}'"))

  # get email count from email_checker
  email = [email["email"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0 :
    return {"email_exist":email_checker[0][0], "email":email_checker[0][1]}
  
  try:
    # convert dictionary to json
    data = str(data.data).replace("'", '"')
    survey_write = execute(f"INSERT INTO \
            `lexical-sol-361019.RA_TOS_SURVEY.survey` \
            (email, data, created_at, updated_at) \
            VALUES ('{data.email}', \
            '{data.data}', \
            '{data.created_at}', \
            '{data.updated_at}')")

    response.set_cookie(key="Survey" + str(data.email),
                        value="accepted",
                        max_age=604800
                        )

    
    return {"message":"success", "data":survey_write}
  
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail="Something went wrong")