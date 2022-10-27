from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import random

from functions.getPhrasesDDB import getPhrasesDDB
from functions.initTable import initTable

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

@app.get(f"/peoplesort/phrases/room")
def getPhrasesByRoom(
    response: Response,
    index: int=0,
    room_id: str="AAAA"
    ):
    try:
        table = initTable()
        all_phrases = getPhrasesDDB(table)
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