from lxml import html
import requests
from pprint import pprint

page = requests.get("http://www.fifa.com/worldcup/matches/")
tree = html.fromstring(page.content)

data = []

matches = tree.find_class('fi-mu fixture')
for match in matches:
    info_els = match.cssselect(".fi-mu__info")
    if len(info_els) == 0:
        continue
    info = info_els[0].text_content()

    home = match.cssselect(".home .fi-t__nText")[0].text_content()
    away = match.cssselect(".away .fi-t__nText")[0].text_content()

    if len(home) < 4 or len(away) < 4:
        continue

    data.append({
        "info": info,
        "home": home,
        "away": away
    })

print(len(data))