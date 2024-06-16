data = {
    "data": {
        "748439531761434676": {
            "money": 49790843062829
        },
        "895175647893291020": {
            "money": 2000000
        },
        "897452848332292107": {
            "money": 2020000
        },
        "1239939075142713364": {
            "money": 1000000
        },
        "321266485068824586": {
            "money": 3100000
        },
        "679561938166218778": {
            "money": 4320000
        },
        "831180234337812500": {
            "money": 1000000
        },
        "584946787014672396": {
            "money": -999999999999999999999999998899999
        },
        "998223623334678538": {
            "money": 1000000
        }
    }
}

# Extract the data dictionary
data_dict = data["data"]

# Sort the dictionary items by the "money" value in descending order
sorted_data = sorted(data_dict.items(), key=lambda item: item[1]["money"], reverse=True)

# Print the sorted data
for user_id, info in sorted_data:
    print(f"User ID: {user_id}, Money: {info['money']}")