import requests
import json

sports = {
        1: "Football",
        2: "Tennis",
        3: "Basketball"
    }

# 1a Liga Portugal - 203
# 1a Liga Basket Portugal - 7368
# 

url = "https://sportscore1.p.rapidapi.com/leagues/203/events"

querystring = {"page":"1"}

headers = {
    'x-rapidapi-host': "sportscore1.p.rapidapi.com",
    'x-rapidapi-key': "46728ebb56msh43b08aa739e7e62p193232jsnffc912d5751e"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)