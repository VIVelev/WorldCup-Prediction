import os
import pickle
from pprint import pprint
from statistics import mean

import numpy as np
import pandas as pd

from .mean_stats import get_average_goals, get_fifa_points
from .player_stats import find_player_stats

__all__ = [
    "get_nbest_scores",
    "predict_proba",
    "xgb_model",
    "team_name_encoder",
]

# # # SET CURRENT FILE DIR # # #
DIR = os.path.abspath(os.path.dirname(__file__))

# # # LOAD ML Utils # # #
with open(os.path.join(DIR, "./ml_data/xgb_model.b"), "rb") as f:
    xgb_model = pickle.load(f)

with open(os.path.join(DIR, "./ml_data/team_name_encoder.b"), "rb") as f:
    team_name_encoder = pickle.load(f)
# # # # # # # # # # # # #

def get_nbest_scores(team_name, n=11, debug=False):
    with open(os.path.join(DIR, "./ml_data/team_players.b"), "rb") as f:
        team_players = pickle.load(f)

    players = team_players[team_name]
    scores = []

    # pprint(players)
    for i in range(len(players)):
        try:
            scores.append(int(players[i][1]))

        except:
            player_stats = find_player_stats(players[i], debug=debug)
            if type(player_stats) is bool:
                try:
                    scores.append(mean(scores))
                    team_players[team_name][i] = [players[i], mean(scores)]
                except:
                    scores.append(60)
                    team_players[team_name][i] = [players[i], 60]
            else:
                player_score = int(player_stats["Overall"])
                scores.append(player_score)
                team_players[team_name][i] = [players[i], player_score]

    # pprint(team_players)
    with open(os.path.join(DIR, "./ml_data/team_players.b"), "wb") as f:
        pickle.dump(team_players, f)

    scores.sort()
    return scores[:n]

def predict_proba(home_team_name, away_team_name):
    feature_names = [
        "Away Team Name",
        "Home Team Name",
        "Home Avg Goals",
        "Away Avg Goals",
        "Home FIFA Points",
        "Away FIFA Points"
    ]

    data = []

    # Away Team Name
    data.append(team_name_encoder.transform([away_team_name])[0])
    # Home Team Name
    data.append(team_name_encoder.transform([home_team_name])[0])

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

    # FIFA Points
    points = get_fifa_points(home_team_name, away_team_name)
    if points:
        # Home FIFA Points
        data.append(points[0])
        # Away FIFA Points
        data.append(points[1])
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
    return xgb_model.predict_proba(df)[0]
