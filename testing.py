import csv
import requests

with open("data.csv", encoding="utf-8") as f:
    r = csv.reader(f)
    data = [row for row in r if row]


def post_data(item):
    headers = {"Content-Type": "application/json"}
    payload = {
        "game_id": item[0],
        "home_team": item[1],
        "away_team": item[2],
        "home_score": item[3],
        "away_score": item[4],
    }
    resp = requests.post(
        "http://localhost:5555", headers=headers, json=payload, timeout=100
    )
    return resp.json()


for item in data:
    print(post_data(item))
