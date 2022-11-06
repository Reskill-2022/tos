from decouple import config
from fastapi import  APIRouter, HTTPException, Request
from auth.schemas.tos_schema import TOS
from starlette.responses import Response
from fastapi.responses import RedirectResponse
from auth.config.settings import execute
from auth.Helpers.helpers import get_cookies, hasher

app = APIRouter()


@app.post("/terms-of-service")
async def read_root(data:TOS, request:Request, response:Response):
  """
  
  """
  # check if all fields are filled

  # get cookies from request
  cookies = get_cookies(request)

  # Hash email from user
  hashed = str(hasher(data.email))
  print("hashed", hashed)
  # Check if hashed email is in cookies keys
  if hashed in cookies.keys():
    return RedirectResponse(url=f'{config("FRONTEND_URL")}', status_code=302)

  if data.email == "" or data.tos_accepted != True:
    raise HTTPException(status_code=400, detail="Please fill all fields")


  # check if email exists
  email_checker = list(execute( f"SELECT * FROM `lexical-sol-361019.RA_TOS_SURVEY.tos` WHERE cookie_hash = '{hashed}'"))

  # get email count from email_checker
  email = [email["email"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0 :
    return {"email_exist":email_checker[0][0], "email":email}

  # insert data
  try:

    tos_write = execute(f"INSERT INTO \
            `lexical-sol-361019.RA_TOS_SURVEY.tos` \
            (email, tos_accepted, created_at, updated_at, cookie_hash) \
            VALUES ('{data.email}', \
            {data.tos_accepted}, \
            '{data.created_at}', \
            '{data.updated_at}', \
              '{hashed}')")
    
    response.set_cookie(key=f"{hashed}", 
                        value="accepted", 
                        max_age=604800
                        )

    return {"message": "Success", 
            "data": tos_write, 
    }

  except Exception as e:
    raise HTTPException(status_code=400, detail={"message": "Something went wrong", "data":e})


# endpoint to get user email
@app.get("/{email}/terms-of-service")
async def get_user_email(email:str, request:Request, response:Response):
  """
  Get user email
  """
  # get cookies from request
  cookies = get_cookies(request)

  # Hash email from user
  hashed = str(hasher(email))

  # Check if hashed email is in cookies keys
  if hashed in cookies.keys():
    return RedirectResponse(url=f'{config("FRONTEND_URL")}', status_code=302)

  # check if email exists
  email_checker = list(execute( f"SELECT * FROM `lexical-sol-361019.RA_TOS_SURVEY.tos` WHERE cookie_hash = '{hashed}'"))

  # get email count from email_checker
  email = [email["email"] for email in email_checker[0][1]]

  if len(email_checker) > 0 and len(email) > 0 :
    response.set_cookie(key=f"{hashed}", 
                    value="accepted", 
                    max_age=604800
                    )
    return {"email_exist":email_checker[0][0], "email":email}

  return {"message": "Email does not exist", "data":email_checker}
