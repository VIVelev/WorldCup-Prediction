from flask import render_template
from app import app
from scraping import get_next_day_matches

from constants import country_codes

@app.route('/')
def index():
    return render_template(
        "index.html", 
        matches=get_next_day_matches, 
        enumerate=enumerate, 
        country_codes=country_codes
    )
