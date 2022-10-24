def getPhrasesDDB(table, level):
    phrases=[]
    response = table.query(
        KeyConditionExpression = "Lvl = :lvl",
        ExpressionAttributeValues={
            ":lvl": level
        }
    )
    if "Items" not in response:
        return {}
    for entry in response["Items"]:
        phrases.append({
            "phrase": entry["Phrase"],
            "lvl": entry["Lvl"]
        })

    return phrases