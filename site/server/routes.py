import pickle

from flask import render_template

from app import app
from constants import country_codes
from scraping import Match, get_next_day_matches

with open("matches.b", "rb") as f:
    matches = pickle.load(f)

@app.route('/')
def index():
    return render_template(
        "index.html", 
        matches=matches,
        enumerate=enumerate, 
        country_codes=country_codes
    )
