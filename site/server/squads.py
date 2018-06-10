import requests
from lxml import html
from pprint import pprint
from constants import country_codes

page = requests.get("https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads")
tree = html.fromstring(page.content)

teams = tree.find_class("wikitable")
data = {}

for team, country in zip(teams, country_codes.keys()):
    players = []
    for player in team.text_content().split('\n\n')[2:-1]:
        player_name = player.split('\n')[3].replace(" (captain)", "")
        players.append(player_name)
    data[country] = players

with open("constants.py", "a") as constants_file:
    constants_file.write("data = {}".format(data.__repr__()))
