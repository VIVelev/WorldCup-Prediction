import datetime
import pickle

from scraping import get_next_day_matches

date = datetime.date.today()
matches = get_next_day_matches(int(date.day)+3)
with open("matches.b", "wb") as f:
    pickle.dump(matches, f)

from match_predictor.main import predict_proba
from match_predictor.mean_stats import get_average_goals

for i in range(len(matches)):
    probs = predict_proba(
        matches[i].home,
        matches[i].away
    )
    avg_goals = get_average_goals(matches[i].home, matches[i].away, 2018, ignore_sides=True)

    matches[i].prob_home = round(probs[1]*100, 2)
    matches[i].prob_away = round(probs[2]*100, 2)
    matches[i].prob_draw = round(probs[0]*100, 2)

    if avg_goals != 0:
        matches[i].avg_goals_home = round(avg_goals[0], 2)
        matches[i].avg_goals_away = round(avg_goals[1], 2)
    else:
        matches[i].avg_goals_home = 0.0
        matches[i].avg_goals_away = 0.0

with open("matches.b", "wb") as f:
    pickle.dump(matches, f)
