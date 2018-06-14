import pickle
import datetime
from flask import render_template, request

from app import app
from constants import country_codes
from scraping import Match, get_next_day_matches

import json

with open("matches.b", "rb") as f:
    matches = pickle.load(f)

results = json.load(open("results.json", "r"))

@app.route('/', methods=["GET", "POST"])
def index():
    colors = []
    final_matches = []
    dates = []

    if request.method == "GET":   
        for match in matches:
            if match.date >= datetime.date.today(): 
                if match.date.strftime("%d.%m.%Y") not in dates:
                    dates.append(match.date.strftime("%d.%m.%Y"))

                if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
                    colors.append(["green", "red", "red"])

                elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
                    colors.append(["red", "green", "red"])

                elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
                    colors.append(["red", "red", "green"])

                else:
                    colors.append(["red", "red", "red"])

                final_matches.append(match)

        return render_template(
            "index.html", 
            matches=final_matches,
            enumerate=enumerate, 
            country_codes=country_codes,
            colors=colors,
            dates=dates
        )

    else:
        want_date = request.form["dates"]
        if want_date != "":
            want_date = want_date.split(".")
            get_date = datetime.date(2018, int(want_date[1]), int(want_date[0]))

        else:
            if datetime.date.today() >  datetime.date(2018, 6, 14):
                get_date = datetime.date.today()
            else:
                get_date = datetime.date(2018, 6, 14)
        
        for match in matches:
            if match.date >= datetime.date.today():      
                if match.date.strftime("%d.%m.%Y") not in dates:
                    dates.append(match.date.strftime("%d.%m.%Y"))

                if match.date == get_date:
                    if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
                        colors.append(["green", "red", "red"])

                    elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
                        colors.append(["red", "green", "red"])

                    elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
                        colors.append(["red", "red", "green"])

                    else:
                        colors.append(["red", "red", "red"])

                    final_matches.append(match)

        return render_template(
            "index.html", 
            matches=final_matches,
            enumerate=enumerate, 
            country_codes=country_codes,
            colors=colors,
            dates=dates
        )

@app.route('/en', methods=["GET", "POST"])
def index_en():
    colors = []
    final_matches = []
    dates = []

    if request.method == "GET":   
        for match in matches:
            if match.date >= datetime.date.today():   
                if match.date.strftime("%d.%m.%Y") not in dates:
                    dates.append(match.date.strftime("%d.%m.%Y"))

                if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
                    colors.append(["green", "red", "red"])

                elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
                    colors.append(["red", "green", "red"])

                elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
                    colors.append(["red", "red", "green"])

                else:
                    colors.append(["red", "red", "red"])

                final_matches.append(match)

        return render_template(
            "index_en.html", 
            matches=final_matches,
            enumerate=enumerate, 
            country_codes=country_codes,
            colors=colors,
            dates=dates
        )

    else:
        want_date = request.form["dates"]
        if want_date != "":
            want_date = want_date.split(".")
            get_date = datetime.date(2018, int(want_date[1]), int(want_date[0]))

        else:
            if datetime.date.today() >  datetime.date(2018, 6, 14):
                get_date = datetime.date.today()
            else:
                get_date = datetime.date(2018, 6, 14)
        
        for match in matches:
            if match.date >= datetime.date.today():       
                if match.date.strftime("%d.%m.%Y") not in dates:
                    dates.append(match.date.strftime("%d.%m.%Y"))

                if match.date == get_date:
                    if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
                        colors.append(["green", "red", "red"])

                    elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
                        colors.append(["red", "green", "red"])

                    elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
                        colors.append(["red", "red", "green"])

                    else:
                        colors.append(["red", "red", "red"])

                    final_matches.append(match)

        return render_template(
            "index_en.html", 
            matches=final_matches,
            enumerate=enumerate, 
            country_codes=country_codes,
            colors=colors,
            dates=dates
        )


@app.route('/past')
def past():
    colors = []
    final_matches = []
    dates = []

    for match in matches:
        if match.date < datetime.date.today():
            if match.date.strftime("%d.%m.%Y") not in dates:
                dates.append(match.date.strftime("%d.%m.%Y"))

            if match.prob_home > match.prob_away and match.prob_home > match.prob_draw:
                colors.append(["green", "red", "red"])

            elif match.prob_draw > match.prob_away and match.prob_draw > match.prob_home:
                colors.append(["red", "green", "red"])

            elif match.prob_away > match.prob_home and match.prob_away > match.prob_draw: 
                colors.append(["red", "red", "green"])

            else:
                colors.append(["red", "red", "red"])

            final_matches.append(match)

    return render_template(
        "past_matches.html", 
        matches=final_matches,
        enumerate=enumerate, 
        country_codes=country_codes,
        colors=colors,
        dates=dates,
        results=results
    )



@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/information_en')
def information_en():
    return render_template('information_en.html')

@app.route('/matches')
def matches_render():
    return render_template('matches.html')

@app.route('/matches_en')
def matches_en():
    return render_template('matches_en.html')
