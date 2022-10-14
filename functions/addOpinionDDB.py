import boto3
import os
from dotenv import load_dotenv

load_dotenv()

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)

table = my_session.resource('dynamodb').Table("IceBreakers-Phrases")

def addOpinionDDB(level, phrase, opinion):
    if opinion:
        table.update_item(
            Key={ "Lvl":level,"Phrase":phrase },
            UpdateExpression = "ADD Like_ :like",
            ExpressionAttributeValues={
                ':like': 1
            }
        )
    else:
        table.update_item(
            Key={ "Lvl":level,"Phrase":phrase  },
            UpdateExpression = "Dislike_ add :dislike",
            ExpressionAttributeValues={
                ':dislike': 1
            }
        )