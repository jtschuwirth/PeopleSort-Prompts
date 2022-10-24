def getPhrasesDDB(table, level):
    phrases=[]
    response = table.query(
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