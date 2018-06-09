from flask import render_template
from app import app
from scraping import get_next_day_matches

from constants import country_codes

@app.route('/')
def index():
    matches = list(get_next_day_matches())
    print(matches)
    return render_template("index.html", matches=matches, enumerate=enumerate, country_codes=country_codes)