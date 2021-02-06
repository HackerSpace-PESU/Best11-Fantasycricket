"""
This module is built as an api wrapper around the scrapyrt process
"""

from typing import List
import requests


class EspnClient:
    """
    A simple wrapper built on the scrapyrt api process
    """

    def __init__(self) -> None:

        self.url = "http://espncricinfo:9080/crawl.json"

    def get_upcoming_dets(self):
        """
        Gets the upcoming matches from the scrapyrt api
        """
        matches = requests.get(
            self.url, params={"spider_name": "espn-live", "start_requests": "true"}
        )

        return matches.json()["items"]

    def get_player_dets(self, players: List[str], team: str):
        """
        Gets and parses player info from the scrapyrt api
        """
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

        player_data = [player for player, _ in player_data if player["role"]]
        return player_data

    def get_match_det(self, player_id: str, role: str, match_type: str):
        """
        Gets and parses match details got fr0om the scrapyrt api
        """
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
            match_det[i] = {
                key: val
                for key, val in match_det[i].items()
                if key not in role_filter_dict[role]
            }
            if role in ["batsman", "all-rounder", "wicket-keeper"]:
                match_det[i]["100"] = match_det[i]["50"] = match_det[i]["duck"] = 0
                if not match_det[i]["runs"]:
                    match_det[i]["runs"] = match_det[i]["boundaries"] = match_det[i][
                        "sixes"
                    ] = 0
                elif match_det[i]["runs"] >= 100:
                    match_det[i]["100"] = 1
                elif match_det[i]["runs"] >= 50:
                    match_det[i]["50"] = 1
                elif match_det[i]["runs"] == 0:
                    match_det[i]["duck"] = 1
            if role in ["bowler", "all-rounder"]:
                match_det[i]["4-wicket-haul"] = match_det[i]["5-wicket-haul"] = 0
                if not match_det[i]["wicket"]:
                    match_det[i]["wicket"] = match_det[i]["Maiden"] = 0
                elif match_det[i]["wicket"] >= 5:
                    match_det[i]["5-wicket-haul"] = 1
                elif match_det[i]["wicket"] >= 4:
                    match_det[i]["4-wicket-haul"] = 1
        return match_det
