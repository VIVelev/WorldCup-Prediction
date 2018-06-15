import os
import pandas as pd

__all__ = [
    "wwmatches",
    "fifa_rankings",
    "get_average_goals",
    "get_fifa_ranks"
]

# # # LOAD DATASETS # # #
DIR = os.path.abspath(os.path.dirname(__file__))
wwmatches = pd.read_csv(os.path.join(DIR, "../wwmatches.csv"))
fifa_rankings = pd.read_csv(os.path.join(DIR, "../fifa_rankings.csv"))
# # # # # # # # # # # # #

def get_average_goals(home, away, ignore_sides=False):
    avg_home = 0
    avg_away = 0
    n = 0
    
    for i in range(len(wwmatches)):
        if (home.lower() in wwmatches.iloc[i]["Home Team Name"].lower() and
            away.lower() in wwmatches.iloc[i]["Away Team Name"].lower()):
                avg_home += wwmatches.iloc[i]["Home Team Goals"]
                avg_away += wwmatches.iloc[i]["Away Team Goals"]
                n+=1
        
        if ignore_sides:
            if (home.lower() in wwmatches.iloc[i]["Away Team Name"].lower() and
                away.lower() in wwmatches.iloc[i]["Home Team Name"].lower()):
                    avg_home += wwmatches.iloc[i]["Away Team Goals"]
                    avg_away += wwmatches.iloc[i]["Home Team Goals"]
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
