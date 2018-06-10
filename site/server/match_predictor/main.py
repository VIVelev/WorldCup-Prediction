import os
import pickle
import numpy as np
import pandas as pd
from .mean_stats import get_average_goals
from .player_stats import find_player_stats

__all__ = [
    "predict_proba",
    "xgb_model",
    "stage_encoder",
    "team_name_encoder",
]

DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(DIR, "../static/ml/xgb_model.b"), "rb") as f:
    xgb_model = pickle.load(f)

with open(os.path.join(DIR, "../static/ml/stage_encoder.b"), "rb") as f:
    stage_encoder = pickle.load(f)

with open(os.path.join(DIR, "../static/ml/team_name_encoder.b"), "rb") as f:
    team_name_encoder = pickle.load(f)

def predict_proba(stage, attendance, home_team_name, home_team_players, away_team_name, away_team_players):
    feature_names = [
        "Stage", "Home Team Name", "Away Team Name",
        "Attendance",
        "Player 1 Overall Diff",
        "Player 2 Overall Diff",
        "Player 3 Overall Diff",
        "Player 4 Overall Diff",
        "Player 5 Overall Diff",
        "Player 6 Overall Diff",
        "Player 7 Overall Diff",
        "Player 8 Overall Diff",
        "Player 9 Overall Diff",
        "Player 10 Overall Diff",
        "Player 11 Overall Diff",
        "Mean Home Team Goals", "Mean Away Team Goals"
    ]

    data = []

    # Stage
    data.append(stage_encoder.transform([stage])[0])
    # Home Team Name
    data.append(team_name_encoder.transform([home_team_name])[0])
    # Away Team Name
    data.append(team_name_encoder.transform([away_team_name])[0])
    # Attendance
    data.append(attendance)

    # Overall
    for i in range(11):
        home_player_overall_score = find_player_stats(home_team_players[i])["Overall"]
        away_player_overall_score = find_player_stats(away_team_players[i])["Overall"]

        data.append(home_player_overall_score-away_player_overall_score)

    mean_goals = get_average_goals(home_team_name, away_team_name)
    # Mean Home Team Goals
    data.append(mean_goals[0])
    # Mean Away Team Goals
    data.append(mean_goals[1])

    df = pd.DataFrame(columns=feature_names)
    data = pd.Series(data, index=feature_names)
    df = df.append(data, ignore_index=True)
    df = df.append(data, ignore_index=True)

    # 0 -> Draw
    # 1 -> Home
    # 2 -> Away
    return xgb_model.predict_proba(df)[0]
