import pickle

from flask import render_template

from app import app
from constants import country_codes
from scraping import Match, get_next_day_matches

with open("matches.b", "rb") as f:
    matches = pickle.load(f)

@app.route('/')
def index():
    for match in matches:
        if type(match.prob_home) is not int:
            match.prob_home = int(match.prob_home * 100)
            match.prob_away = int(match.prob_away * 100)
            match.prob_draw = int(match.prob_draw * 100)
        
    return render_template(
        "index.html", 
        matches=matches,
        enumerate=enumerate, 
        country_codes=country_codes
    )

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/matches')
def matches_render():
    return render_template('matches.html')