def getPhrasesDDB(table):
    phrases=[]
    response = table.scan()
    if "Items" not in response:
        return {}
    for entry in response["Items"]:
        phrases.append({
            "max": entry["max"],
            "min": entry["min"]
        })

    return phrases