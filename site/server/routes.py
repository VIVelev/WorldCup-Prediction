from flask import render_template
from app import app
from scraping import get_next_day_matches, Match
import json

from constants import country_codes

with open("matches.json", "r") as matches_file:
    matches = json.load(matches_file)

matches = list(map(lambda o: Match.from_dict(o), matches))

@app.route('/')
def index():
    return render_template(
        "index.html", 
        matches=matches,
        enumerate=enumerate, 
        country_codes=country_codes
    )
