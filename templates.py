def header_template(team1, team2, score1, score2):
    return f"""
### {team1} {score1}-{score2} {team2}
"""


def match_score_template(map, score1, score2):
    return f"""**{map}**: {score1}-{score2}
"""


def filler_template(tournament,link):
    return f"""[{tournament}]({link})
---
"""


def map_template(map_index, map_name, team1, team2, players):
    team1_players = "\n".join([stat_template(player) for player in players[0]])
    team2_players = "\n".join([stat_template(player) for player in players[1]])

    return f"""### Map {map_index}: {map_name}

---
{team1}|ACS|K|D|A
---|---|---|---|---
{team1_players}
---
{team2}|ACS|K|D|A
---|---|---|---|---
{team2_players}
"""


def stat_template(player):
    return f"[{player['name']}]({player['link']}) **{player['agent']}**|{player['acs']}|{player['kills']}|{player['deaths']}|{player['assists']}"
