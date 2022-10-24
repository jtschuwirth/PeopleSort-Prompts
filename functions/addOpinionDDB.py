def addOpinionDDB(table, level, phrase, opinion):
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
            UpdateExpression = "ADD Dislike_ :dislike",
            ExpressionAttributeValues={
                ':dislike': 1
            }
        )