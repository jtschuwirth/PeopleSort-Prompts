
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)
def getPhrasesDDB(level):
    phrases=[]
    response = my_session.client("dynamodb").query(
        TableName="IceBreakers-Phrases",
        KeyConditionExpression = "Lvl = :lvl",
        ExpressionAttributeValues={
            ":lvl": { "N": str(level) }
        }
    )
    if "Items" not in response:
        return {}
    for entry in response["Items"]:
        phrases.append({
            "phrase": entry["Phrase"]["S"],
            "lvl": entry["Lvl"]["N"]
        })

    return phrases