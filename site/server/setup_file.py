import pickle

from match_predictor.main import predict_proba
from match_predictor.mean_stats import get_average_goals
from scraping import get_next_day_matches

matches = []
for match in get_next_day_matches(4):
    probs = predict_proba(
        match.stage, 50_000,
        match.home, match.away
    )
    avg_goals = get_average_goals(match.home, match.away, ignore_sides=True)

    match.prob_home = probs[1]
    match.prob_away = probs[2]
    match.prob_draw = probs[0]

    if avg_goals != 0:
        match.avg_goals_home = avg_goals[0]
        match.avg_goals_away = avg_goals[1]
    else:
        match.avg_goals_home = 0.0
        match.avg_goals_away = 0.0

    matches.append(match)
    print(match)

with open("matches.b", "wb") as f:
    pickle.dump(matches, f)
