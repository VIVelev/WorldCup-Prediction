import datetime
import re
from pprint import pprint

import requests
from lxml import html

from constants import groups

class Match:
    def __init__(self, home="", away="", home_goals=-1, away_goals=-1, date="", time="", stage=""):
        self.home = home
        self.away = away
        self.home_goals = home_goals
        self.away_goals = away_goals

        if date != "":
            self.date = datetime.datetime.strptime(date, "%d %b %Y").date() # eg. "07 Jun 2018"
        else:
            self.date = datetime.date.today()
        self.time = time
        self.stage = "Group " + stage

        self.prob_home = 0
        self.prob_away = 0
        self.prob_draw = 0

        self.avg_goals_home = 0
        self.avg_goals_away = 0
    
    def __repr__(self):
        return "{stage}: {home} vs {away} Playing on {date} at {time}".format(
            home=self.home,
            away=self.away,
            date=self.date.strftime("%d %b %Y"),
            time=self.time,
            stage=self.stage
        )
    
    def __iter__(self):
        yield 'date', self.date.strftime("%Y-%m-%d")
        for key, value in self.__dict__.items():
            if key == 'date':
                continue
            yield key, value
    
    @classmethod
    def from_dict(cls, dct):
        obj = cls()
        for key, value in dct.items():
            setattr(obj, key, value)
        obj.date = datetime.datetime.strptime(dct['date'], "%Y-%m-%d").date()
        
        return obj

def get_next_day_matches(days):
    first_day = datetime.date(2018, 6, 14)
    tomorrow = datetime.timedelta(days=days)
    
    page = requests.get("http://www.fifa.com/worldcup/matches/")
    tree = html.fromstring(page.content)

    matches = tree.find_class('fi-mu result') + tree.find_class('fi-mu live') + tree.find_class('fi-mu fixture')
    final_matches = []
    for match in matches:
        info_els = match.cssselect(".fi-mu__info")
        if len(info_els) == 0:
            continue
        info = info_els[0].text_content()
        info = re.sub("[\r\n]", '', info)
        info = list(filter(lambda i: i != '', info.split(' ')))

        date = " ".join(info[:3])
        time = info[4]
        group = info[11] if info[11] in groups else "Round of 16"
        # print(date, time, group)
        # print("-" * 30)

        home = match.cssselect(".home .fi-t__nText")[0].text_content()
        away = match.cssselect(".away .fi-t__nText")[0].text_content()

        if len(home) < 4 or len(away) < 4:
            continue
        
        result = match.cssselect(".fi-s__scoreText")[0].text_content()
        if "-" in result:
            home_goals, away_goals = result.split("-")
            home_goals, away_goals = int(home_goals), int(away_goals)
        else:
            home_goals = away_goals = -1

        match = Match(home=home, away=away, home_goals=home_goals, away_goals=away_goals, date=date, time=time, stage=group)

        if match.date >= first_day and match.date <= first_day + tomorrow:
            final_matches.append(match)

    return final_matches
