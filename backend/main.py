import json
from fastapi import FastAPI

PATH = "data/nfl_data.json"


app = FastAPI()


@app.get("/level-1/data")
async def get_data():
    with open(file=PATH, mode="r") as raw_file:
        data = json.load(raw_file)
    return data


@app.get("/level-1/teams")
async def get_teams():
    with open(file=PATH, mode="r") as raw_file:
        data = json.load(raw_file)
    return data["teams"]
