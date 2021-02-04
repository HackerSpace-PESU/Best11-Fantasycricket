import requests
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict
from typing import TypeVar, List, Union, Optional


class Player(TypedDict):
    name: str
    role: str
    image: str
    player_id: str
    team: str


class Match(TypedDict):
    runs: Optional[int]
    boundaries: Optional[int]
    sixes: Optional[int]
    wicket: Optional[int]
    Maiden: Optional[int]
    Catch: Optional[int]
    Stump: Optional[int]
    match_id: str


class Squad(TypedDict):

    name: str
    player_id: str


class Upcoming(TypedDict):

    team1: str
    team2: str
    match_id: str
    team1_squad: List[Squad]
    team2_squad: List[Squad]


class espn_scrapyrt_client:
    def __init__(self) -> None:

        self.url = "http://localhost:9080/crawl.json"

    def get_upcoming_dets(self) -> List[Upcoming]:

        matches = requests.get(
            self.url, params={"spider_name": "espn-live", "start_requests": "true"}
        )

        return matches.json()["items"]

    def get_player_dets(self, players: List[str], team: str) -> List[Player]:

        player_data = []
        for player in players:
            player_data.append(
                (
                    requests.get(
                        self.url,
                        params={
                            "spider_name": "espn-players",
                            "url": "https://www.espncricinfo.com/ci/content/player/"
                            + str(player)
                            + ".html",
                        },
                    ).json()["items"][0],
                    player,
                )
            )
        for player, player_id in player_data:
            if not player["role"]:
                continue
            if "wicketkeeper" in player["role"].lower():
                player["role"] = "wicket-keeper"
            elif "allrounder" in player["role"].lower():
                player["role"] = "all-rounder"
            elif "bowler" in player["role"].lower():
                player["role"] = "bowler"
            else:
                player["role"] = "batsman"
            player["team"] = team
            player["player_id"] = player_id

        player_data = [player for player, _ in player_data if player["role"] != None]
        return player_data

    def get_match_det(self, player_id: str, role: str, match_type: str) -> List[Match]:

        role_filter_dict = {
            "batsman": ["Catch", "Stump", "wicket", "Maiden"],
            "bowler": ["Catch", "Stump", "runs", "boundaries", "sixes"],
            "all-rounder": ["Catch", "Stump"],
            "wicket-keeper": ["wicket", "Maiden"],
        }
        match_det = requests.get(
            self.url,
            params={
                "spider_name": "espn-matches",
                "url": "https://stats.espncricinfo.com/ci/engine/player/"
                + player_id
                + ".html?class="
                + match_type
                + ";orderby=start;orderbyad=reverse;template=results;type=allround;view=match",
            },
        ).json()["items"]
        for i, _ in enumerate(match_det):
            match_det[i] = dict(
                [
                    (key, val)
                    for key, val in match_det[i].items()
                    if key not in role_filter_dict[role]
                ]
            )
            if role == "batsman":
                match_det[i]["100"] = match_det[i]["50"] = match_det[i]["duck"] = 0
                if match_det[i]["runs"] >= 100:
                    match_det[i]["100"] = 1
                elif match_det[i]["50"] >= 50:
                    match_det[i]["50"] = 1
                elif match_det[i]["runs"] == 0:
                    match_det[i]["duck"] = 1
            elif role == "bowler":
                match_det[i]["4-wicket-haul"] = match_det[i]["5-wicket-haul"] = 0
                if match_det[i]["wicket"] >= 5:
                    match_det[i]["5-wicket-haul"] = 1
                elif match_det[i]["4-wicket-haul"] >= 4:
                    match_det[i]["4-wicket-haul"] = 1
            elif role == "all-rounder":
                match_det[i]["4-wicket-haul"] = match_det[i]["5-wicket-haul"] = 0
                match_det[i]["100"] = match_det[i]["50"] = match_det[i]["duck"] = 0
                if match_det[i]["runs"] >= 100:
                    match_det[i]["100"] = 1
                elif match_det[i]["50"] >= 50:
                    match_det[i]["50"] = 1
                elif match_det[i]["runs"] == 0:
                    match_det[i]["duck"] = 1
                if match_det[i]["wicket"] >= 5:
                    match_det[i]["5-wicket-haul"] = 1
                elif match_det[i]["4-wicket-haul"] >= 4:
                    match_det[i]["4-wicket-haul"] = 1
            elif role == "wicket-keeper":
                match_det[i]["100"] = match_det[i]["50"] = match_det[i]["duck"] = 0
                if match_det[i]["runs"] >= 100:
                    match_det[i]["100"] = 1
                elif match_det[i]["50"] >= 50:
                    match_det[i]["50"] = 1
                elif match_det[i]["runs"] == 0:
                    match_det[i]["duck"] = 1
        return match_det
