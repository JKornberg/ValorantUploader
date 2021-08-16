from bs4 import BeautifulSoup
from templates import *
import requests
import requests.auth
import argparse
import praw
from cred_reddit import *


def main(url):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    games = soup.find_all("div", {"class": "vm-stats-game"})
    games = [game for game in games if game['data-game-id'] != 'all']

    teams = [team.text.strip() for team in soup.select("div.wf-title-med")]
    results = soup.find(
        'div', {'class': 'match-header-vs-score'}).find_all('span')
    match_score = [int(result.text.strip())
                   for result in [results[0], results[2]]]

    header = header_template(
        teams[0], teams[1], match_score[0], match_score[1])
    matches = []
    for game_index, game in enumerate(games):

        score_parents = game.find_all('div', {'class': 'score'})
        game_scores = [score.text.strip() for score in score_parents]
        map = next(game.find('div', {'class': 'map'}
                             ).find('span').children).strip()
        match_score = match_score_template(map, game_scores[0], game_scores[1])
        tables = game.find_all('table', 'wf-table-inset')
        players = [[], []]

        for team_index, table in enumerate(tables):
            rows = table.find_all('tr')
            for row in rows:
                player = row.find('td', {'class': 'mod-player'})
                if (not player):
                    continue
                link = 'https://vlr.gg' + player.find('a')['href']
                agent = row.find('img')['title'].title()
                name = player.find('div', {'class': 'text-of'}).text.strip()
                acs = row.find(
                    'td', {'class': 'mod-stat'}).find('span').text.strip()
                k = row.find(
                    'td', {'class': 'mod-vlr-kills'}).find('span').text.strip()
                d = row.find(
                    'td', {'class': 'mod-vlr-deaths'}).find('span').text.strip().strip("/")
                a = row.find(
                    'td', {'class': 'mod-vlr-assists'}).find('span').text.strip()
                players[team_index].append(
                    {'name': name, 'link': link, 'kills': k, 'deaths': d, 'assists': a, 'acs': acs, 'agent': agent})
        map_details = map_template(
            game_index + 1, map, teams[0], teams[1], players)
        matches.append("\n".join([match_score, map_details]))
        matches_string = "\n".join(matches)
    with open("test.txt", "w") as doc:
        doc.write("\n".join([header, matches_string]))


def reddit_api():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username,
    )
