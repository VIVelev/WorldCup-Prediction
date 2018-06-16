import os
import random
from math import sqrt

import pandas as pd

__all__ = [
    "stats",
    "clean",
    "find_start_index",
    "find_end_index",
    "find_player_stats",
]

# # # LOAD PLAYERS' STATS # # #
DIR = os.path.abspath(os.path.dirname(__file__))
stats = pd.read_csv(os.path.join(DIR, "./ml_data/PlayersStats.csv"), low_memory=False)
# # # # # # # # # # # # # # # #

def clean(x):
    x = x.lower().strip().split(" ")

    if len(x) == 1:
        x = x[0]

    elif len(x) == 2:
        if "." in x[0]:
            x = x[1]
        elif "." in x[1]:
            x = x[0]
        else:
            x = x[0] + x[1]

    elif len(x) == 3:
        if "." in x[0]:
            x = x[1] + x[2]
        elif "." in x[1]:
            x = x[0] + x[2]
        elif "." in x[2]:
            x = x[0] + x[1]
        else:
            x = x[0] + x[1] + x[2]

    elif len(x) == 4:
        if "(" in x[3] or ")" in x[3]:
            if "." in x[0]:
                x = x[1] + x[2]
            elif "." in x[1]:
                x = x[0] + x[2]
            elif "." in x[2]:
                x = x[0] + x[1]
            else:
                x = x[0] + x[1] + x[2]
        else:
            if "." in x[0]:
                x = x[1] + x[2] + x[3]
            elif "." in x[1]:
                x = x[0] + x[2] + x[3]
            elif "." in x[2]:
                x = x[0] + x[1] + x[3]
            elif "." in x[3]:
                x = x[0] + x[1] + x[2]
            else:
                x = x[0] + x[1] + x[2] + x[3]
            
    else:
        pass
    
    return x

def find_start_index(name):
    name = clean(name)
    i = 0
    jump_step = int(sqrt(len(stats)))
    
    while i < len(stats) and name[0] > clean(stats["Name"][i])[0]:
        i += jump_step
    
    if i >= jump_step:
        i -= jump_step

    return i

def find_end_index(name):
    name = clean(name)
    i = len(stats)-1
    jump_step = int(sqrt(len(stats)))
    
    while i >= 0 and name[0] < clean(stats["Name"][i])[0]:
        i -= jump_step

    if i < len(stats)-jump_step:
        i += jump_step

    return i

def find_player_stats(name, debug=False):
    best_match_index = -1
            
    for i in range(find_start_index(name), find_end_index(name)):      
        if name == stats["Name"][i]:
            best_match_index = i
            
    if best_match_index != -1:
        if debug:
            print("Search: ", name, " | ", "Best match: ", stats.iloc[best_match_index]["Name"])
        return stats.iloc[best_match_index]
        
    else:
        return False
