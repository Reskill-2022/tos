from fastapi import Request
import hashlib


# function to get cookies from request
def get_cookies(request:Request):
  cookies = request.cookies
  return cookies

# function to hash email to 8 characters
def hasher(email):
  return hashlib.sha256(email.encode()).hexdigest()[:]