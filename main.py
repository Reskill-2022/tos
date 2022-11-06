import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Apps
from auth.apps.tos import app as tos
# from auth.apps.survey import app as survey

app = FastAPI(    
    title="TOS API",
    description="provides acces to store user email after they accept terms of service",
    version="1.0",
    docs_url='/tos/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url=None)

load_dotenv() 

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(tos,tags=["tos"])
# app.include_router(survey,tags=["survey"])

@app.get("/tos/health")
async def root():
    return "Healthy"

if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)