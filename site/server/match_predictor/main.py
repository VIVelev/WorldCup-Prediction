import os
import pickle
from pprint import pprint

import numpy as np
import pandas as pd

from .mean_stats import find_rank, get_average_goals

__all__ = [
    "model",
    "team_name_encoder",
    "predict_proba",
]

# # # SET CURRENT FILE DIR # # #
DIR = os.path.abspath(os.path.dirname(__file__))

# # # LOAD ML Utils # # #
with open(os.path.join(DIR, "./ml_data/model.b"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(DIR, "./ml_data/team_name_encoder.b"), "rb") as f:
    team_name_encoder = pickle.load(f)
# # # # # # # # # # # # #

def predict_proba(home_team_name, away_team_name):
    feature_names = [
        "Away Team Name",
        "Home Team Name",

        "home_rank",
        "home_total_points",
        "home_cur_year_avg",
        "home_cur_year_avg_weighted",
        
        "away_rank",
        "away_total_points",
        "away_cur_year_avg",
        "away_cur_year_avg_weighted",
        
        "Home Avg Goals",
        "Away Avg Goals"
    ]

    data = []

    # Away Team Name
    data.append(team_name_encoder.transform([away_team_name])[0])
    # Home Team Name
    data.append(team_name_encoder.transform([home_team_name])[0])

    home_team_rank = find_rank(home_team_name, 2018)
    away_team_rank = find_rank(away_team_name, 2018)

    # home_rank, home_total_points, home_cur_year_avg, home_cur_year_avg_weighted
    data.append(home_team_rank["rank"])
    data.append(home_team_rank["total_points"])
    data.append(home_team_rank["cur_year_avg"])
    data.append(home_team_rank["cur_year_avg_weighted"])

    # away_rank, away_total_points, away_cur_year_avg, away_cur_year_avg_weighted
    data.append(away_team_rank["rank"])
    data.append(away_team_rank["total_points"])
    data.append(away_team_rank["cur_year_avg"])
    data.append(away_team_rank["cur_year_avg_weighted"])

    # Avg Goals
    avg_goals = get_average_goals(home_team_name, away_team_name, 2018)
    if avg_goals:
        # Home Avg Goals
        data.append(avg_goals[0])
        # Away Avg Goals
        data.append(avg_goals[1])
    else:
        data.append(0.0)
        data.append(0.0)

    # Aggregating data
    df = pd.DataFrame(columns=feature_names)
    data = pd.Series(data, index=feature_names)
    df = df.append(data, ignore_index=True)
    df = df.append(data, ignore_index=True)

    # 0 -> Draw
    # 1 -> Home
    # 2 -> Away
    return model.predict_proba(df)[0]
