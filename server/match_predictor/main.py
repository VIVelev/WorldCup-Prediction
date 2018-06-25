import os
import pickle

import numpy as np
import pandas as pd

from .mean_stats import find_rank, get_average_goals

__all__ = [
    "FEATURE_NAMES",

    "model",
    "team_name_encoder",

    "matches2k18",
    "dataset",

    "get_X_y",
    "get_X_y_2k18",
    "train",
    "predict_proba",
]

FEATURE_NAMES = [
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

# # # SET CURRENT FILE DIR # # #
DIR = os.path.abspath(os.path.dirname(__file__))

# # # LOAD ML Utils # # #
with open(os.path.join(DIR, "./ml_data/model.b"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(DIR, "./ml_data/team_name_encoder.b"), "rb") as f:
    team_name_encoder = pickle.load(f)
# # # # # # # # # # # # #

# # # LOAD 2018 MATCHES # # #
with open(os.path.join(DIR, "../matches.b"), "rb") as f:
    matches2k18 = pickle.load(f)
# # # # # # # # # # # # # # #

# # # LOAD THE DATSET # # # 
dataset = pd.read_csv(os.path.join(DIR, "./ml_data/final.csv"))
# # # # # # # # # # # # # #

def get_X_y():
    X = dataset[FEATURE_NAMES]
    X["Away Team Name"] = team_name_encoder.transform(X["Away Team Name"])
    X["Home Team Name"] = team_name_encoder.transform(X["Home Team Name"])

    y = []
    for i in range(len(dataset)):
        home_team_goals = dataset["Home Team Goals"][i]
        away_team_goals = dataset["Away Team Goals"][i]
        
        if home_team_goals > away_team_goals:
            y.append(1)
        elif home_team_goals < away_team_goals:
            y.append(2)
        else:
            y.append(0)

    return X, y

def get_X_y_2k18():
    X_2k18, y_2k18 = pd.DataFrame(columns=FEATURE_NAMES), []

    for match in matches2k18:
        current_data = []

        # Away Team Name
        current_data.append(team_name_encoder.transform([match.away])[0])
        # Home Team Name
        current_data.append(team_name_encoder.transform([match.home])[0])

        home_team_rank = find_rank(match.home, 2018)
        away_team_rank = find_rank(match.away, 2018)

        # home_rank, home_total_points, home_cur_year_avg, home_cur_year_avg_weighted
        current_data.append(home_team_rank["rank"])
        current_data.append(home_team_rank["total_points"])
        current_data.append(home_team_rank["cur_year_avg"])
        current_data.append(home_team_rank["cur_year_avg_weighted"])

        # away_rank, away_total_points, away_cur_year_avg, away_cur_year_avg_weighted
        current_data.append(away_team_rank["rank"])
        current_data.append(away_team_rank["total_points"])
        current_data.append(away_team_rank["cur_year_avg"])
        current_data.append(away_team_rank["cur_year_avg_weighted"])

        # Avg Goals
        avg_goals = get_average_goals(match.home, match.away, 2018)
        if avg_goals:
            # Home Avg Goals
            current_data.append(avg_goals[0])
            # Away Avg Goals
            current_data.append(avg_goals[1])
        else:
            current_data.append(0.0)
            current_data.append(0.0)

        # Prepare data
        current_data = pd.Series(current_data, index=FEATURE_NAMES)
        if match.home_goals > match.away_goals:
            y = 1
        elif match.home_goals < match.away_goals:
            y = 2
        else:
            y = 0

        for _ in range(len(dataset)//1000):
            X_2k18 = X_2k18.append(current_data, ignore_index=True)
            y_2k18.append(y)

    return X_2k18, y_2k18

def train():
    X, y = get_X_y()
    X_2k18, y_2k18 = get_X_y_2k18()
    X = X[len(X)//2:]
    y = y[len(y)//2:]
    X = X.append(X_2k18, ignore_index=True)
    y = y + y_2k18

    model.fit(X, y)

def predict_proba(home_team_name, away_team_name):
    train()

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

    # Aggregate data
    df = pd.DataFrame(columns=FEATURE_NAMES)
    data = pd.Series(data, index=FEATURE_NAMES)
    df = df.append(data, ignore_index=True)
    df = df.append(data, ignore_index=True)

    # 0 -> Draw
    # 1 -> Home
    # 2 -> Away
    return model.predict_proba(df)[0]
