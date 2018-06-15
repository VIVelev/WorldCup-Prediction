import os
import pandas as pd

__all__ = [
    "matches",
    "fifa_rankings",
    "get_average_goals",
    "get_fifa_ranks"
]

# # # LOAD DATASETS # # #
DIR = os.path.abspath(os.path.dirname(__file__))
matches = pd.read_csv(os.path.join(DIR, "../final.csv"))
fifa_rankings = pd.read_csv(os.path.join(DIR, "../fifa_rankings.csv"))
# # # # # # # # # # # # #

def get_average_goals(home, away, ignore_sides=False):
    avg_home = 0
    avg_away = 0
    n = 0
    
    for i in range(len(matches)):
        if (home.lower() in matches["Home Team Name"][i].lower() and
            away.lower() in matches["Away Team Name"][i].lower()):
                avg_home += matches["Home Team Goals"][i]
                avg_away += matches["Away Team Goals"][i]
                n+=1
        
        if ignore_sides:
            if (home.lower() in matches["Away Team Name"][i].lower() and
                away.lower() in matches["Home Team Name"][i].lower()):
                    avg_home += matches["Away Team Goals"][i]
                    avg_away += matches["Home Team Goals"][i]
                    n+=1

    if n > 0:
        return [
            avg_home/n,
            avg_away/n
        ]

    else:
        return False

def get_fifa_ranks(home_team_name, away_team_name):
    try:
        home_rank = float(fifa_rankings[fifa_rankings["Team"] == home_team_name]["Position"])
        away_rank = float(fifa_rankings[fifa_rankings["Team"] == away_team_name]["Position"])

        return [
            home_rank,
            away_rank
        ]

    except:
        return False
