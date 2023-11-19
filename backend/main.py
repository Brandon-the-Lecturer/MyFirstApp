import json
import pandas as pd
from fastapi import FastAPI

PATH = "data/nfl_data.json"


app = FastAPI()


def FileHanlder():
    with open(file=PATH, mode="r") as raw_file:
        data = json.load(raw_file)
    return data


@app.get("/level-1/data")
async def get_data():
    return FileHanlder()


@app.get("/level-1/teams")
async def get_teams():
    data = FileHanlder()
    return data["teams"]


@app.get("/level-2/stats")
async def get_stats(team_type: str = "team"):
    raw_data = FileHanlder()

    raw_data_df = pd.DataFrame(raw_data["games"])

    stats = raw_data_df.groupby(team_type)[["points_scored", "points_allowed"]].mean()
    stats[team_type] = stats.index
    stats.sort_values("points_scored", ascending=False, inplace=True)
    stats.reset_index(drop=True, inplace=True)
    stats.index += 1

    return stats.to_json(orient="index")
