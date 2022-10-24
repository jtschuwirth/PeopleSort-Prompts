from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
import random
import boto3
import os
from dotenv import load_dotenv

from functions.getPhrasesDDB import getPhrasesDDB
from functions.addOpinionDDB import addOpinionDDB

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://jtschuwirth.xyz",
    "https://www.jtschuwirth.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)

table_name = os.environ['TABLE_NAME']
table = my_session.resource('dynamodb').Table(table_name)

@app.get("/icebreakers/phrases")
def getPhrases(
    response: Response,
    n: int=1,
    level:int=1
    ):
    try:
        if level not in [1,2,3]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="level can only be 1, 2 or 3")
        all_phrases = getPhrasesDDB(table, level)
        if len(all_phrases)==0:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error retriving phrases")
        elif n > len(all_phrases) :
            n=len(all_phrases)
        phrases = random.sample(all_phrases, k=n)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return phrases

class Opinion(BaseModel):
    level:int
    phrase:str
    opinion:int

@app.post("/icebreakers/opinion")
def addOpinion(
    data: Opinion,
    response: Response
    ):
    try:
        addOpinionDDB(table, data.level, data.phrase, data.opinion)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return "Success"

#uvicorn lambda_function:app --reload --port 8081
lambda_handler = Mangum(app, lifespan="off")