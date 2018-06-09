from lxml import html
import requests
from pprint import pprint
from datetime import datetime, date, timedelta
import re

from constants import groups

class Match:
    def __init__(self, home, away, date, time, group):
        self.home = home
        self.away = away
        self.date = datetime.strptime(date, "%d %b %Y").date() # eg. "07 Jun 2018"
        self.time = time
        self.group = group

        self.prob_home = 60
        self.prob_away = 10
        self.prob_draw = 30

        self.ml_predict_home = 60
        self.ml_predict_away = 10
        self.ml_predict_draw = 30

        self.avg_goals_home = 1.5
        self.avg_goals_away = 1

        self.twitter_posts_home = 40
        self.twitter_posts_away = 20
        self.twitter_posts_draw = 10
    
    def __repr__(self):
        return "Group {group}: {home} vs {away} Playing on {date} at {time}".format(
            home=self.home,
            away=self.away,
            date=self.date.strftime("%d %b %Y"),
            time=self.time,
            group=self.group
        )

def get_next_day_matches():
    global date
    tomorrow = date.today() + timedelta(days=7)
    
    page = requests.get("http://www.fifa.com/worldcup/matches/")
    tree = html.fromstring(page.content)

    data = []

    matches = tree.find_class('fi-mu fixture')
    for match in matches:
        info_els = match.cssselect(".fi-mu__info")
        if len(info_els) == 0:
            continue
        info = info_els[0].text_content()
        info = re.sub("[\r\n]", '', info)
        info = list(filter(lambda i: i != '', info.split(' ')))

        date = " ".join(info[:3])
        time = info[4]
        group = info[11] if info[11] in groups else None
        # print(date, time, group)
        # print("-" * 30)

        home = match.cssselect(".home .fi-t__nText")[0].text_content()
        away = match.cssselect(".away .fi-t__nText")[0].text_content()

        if len(home) < 4 or len(away) < 4:
            continue
        
        match = Match(home=home, away=away, date=date, time=time, group=group)
        
        if match.date == tomorrow:
            yield match