import os
import pandas as pd

__all__ = [
    "matches",
    "fifa_ranking",
    "get_average_goals",
    "find_rank",
]

# # # LOAD DATASETS # # #
DIR = os.path.abspath(os.path.dirname(__file__))
matches = pd.read_csv(os.path.join(DIR, "../final.csv"))
fifa_ranking = pd.read_csv(os.path.join(DIR, "../fifa_ranking.csv"))
# # # # # # # # # # # # #

def get_average_goals(home, away, year, ignore_sides=False):
    avg_home = 0
    avg_away = 0
    n = 0
    i = 0
    
    while i < len(matches) and matches["Year"][i] <= year:
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
                
        i+=1

    if n > 0:
        return [
            avg_home/n,
            avg_away/n
        ]

    else:
        return False

def find_rank(team_name, year):
    l = 0
    r = len(fifa_ranking)-1
    year_i = -1
    
    while (l < r):
        mid = (l+r)//2
        if fifa_ranking["year"][mid] > year:
            r = mid-1
        elif fifa_ranking["year"][mid] < year:
            l = mid+1
        else:
            year_i = mid
            break
            
    if year_i == -1:
        return False
    
    tmp = fifa_ranking["year"][year_i]
    while year_i >= 0 and fifa_ranking["year"][year_i] == tmp:
        year_i-=1
        
    year_i+=1
    
    for i in range(year_i, len(fifa_ranking)):
        if fifa_ranking["country"][i] == team_name:
            return fifa_ranking.iloc[i]
        
    return False
