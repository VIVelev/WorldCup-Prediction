from .mean_stats import get_average_goals

__all__ = [
    "predict_proba",
]

def predict_proba(home_team_name, home_team_players, away_team_name, away_team_players):
    return get_average_goals(home_team_name, away_team_name)
