import pickle

from flask import render_template

from app import app
from constants import country_codes
from scraping import Match, get_next_day_matches

with open("matches.b", "rb") as f:
    matches = pickle.load(f)

@app.route('/')
def index():
    colors = []

    for match in matches:

        if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
            colors.append(["green", "red", "red"])

        elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
            colors.append(["red", "green", "red"])

        elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
            colors.append(["red", "red", "green"])

        else:
            colors.append(["red", "red", "red"])

        if type(match.prob_home) is not int:
            match.prob_home = int(match.prob_home * 100)
            match.prob_away = int(match.prob_away * 100)
            match.prob_draw = int(match.prob_draw * 100)


    print(colors)

    return render_template(
        "index.html", 
        matches=matches,
        enumerate=enumerate, 
        country_codes=country_codes,
        colors=colors
    )

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/matches')
def matches_render():
    return render_template('matches.html')