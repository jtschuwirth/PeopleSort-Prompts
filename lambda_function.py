from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
import random

from functions.getPhrasesDDB import getPhrasesDDB
from functions.addOpinionDDB import addOpinionDDB
from functions.initTable import initTable

import os
from dotenv import load_dotenv
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

game=os.environ.get("GAME")

@app.get(f"/{game}/phrases")
def getPhrases(
    response: Response,
    n: int=1,
    level:int=1
    ):
    try:
        table = initTable()
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

@app.post(f"/{game}/opinion")
def addOpinion(
    data: Opinion,
    response: Response
    ):
    try:
        table = initTable()
        addOpinionDDB(table, data.level, data.phrase, data.opinion)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return "Success"

@app.get(f"/{game}/phrases/room")
def getPhrasesByRoom(
    response: Response,
    index: int=1,
    level: int=1,
    room_id: str="AAAA"
    ):
    try:
        table = initTable()
        if level not in [1,2,3]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="level can only be 1, 2 or 3")
        all_phrases = getPhrasesDDB(table, level)
        if len(all_phrases)==0:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error retriving phrases")
        random.seed(room_id)
        random.shuffle(all_phrases)
        phrases = [all_phrases[index%len(all_phrases)]]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return phrases

#uvicorn lambda_function:app --reload --port 8081
lambda_handler = Mangum(app, lifespan="off")