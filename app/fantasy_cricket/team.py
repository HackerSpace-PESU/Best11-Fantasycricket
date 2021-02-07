"""
This module defines the teams class which is generic over the classes in fantasy_leagues module
"""

from typing import List, Optional
import numpy as np
from sklearn.linear_model import LinearRegression
from app.fantasy_cricket.scrapyrt_client import EspnClient


class Team:
    """
    A generic class built over the league classes in fantasy_leagues.py
    """

    name: Optional[str] = None

    batting_dict = {}
    bowling_dict = {}
    wk_dict = {}

    def __init__(self, team1: str, team2: str) -> None:

        self.fantasy_team = {team1: [], team2: []}
        self.team1 = team1
        self.team2 = team2
        self.espn = EspnClient()

    def get_fantasy_team(self):
        """
        Get the fantasy team predicted including captains
        """
        vice_captain, captain = self.get_captain_vicecaptain()
        for player in self.fantasy_team[self.team1] + self.fantasy_team[self.team2]:
            if player == captain:
                player["captain"] = "(C)"
            elif player == vice_captain:
                player["captain"] = "(VC)"
            else:
                player["captain"] = ""
        return self.fantasy_team[self.team1] + self.fantasy_team[self.team2]

    def get_captain_vicecaptain(self):
        """
        Get captains and vice captains only
        """
        return sorted(
            self.fantasy_team[self.team1] + self.fantasy_team[self.team2],
            key=lambda i: i["score"],
        )[-2:]

    def get_score(self, role: str, match_type: str, score_info) -> float:
        """
        Function to predict the fantasy league score of each player
        """
        player_scores = {}
        for score_data in score_info:
            if role == "batsman":
                player_scores[score_data["match_id"]] = sum(
                    self.batting_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key != "match_id"
                )
            elif role == "bowler":
                player_scores[score_data["match_id"]] = sum(
                    self.bowling_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key != "match_id"
                )
            elif role == "all-rounder":
                player_scores[score_data["match_id"]] = sum(
                    self.batting_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key
                    not in [
                        "match_id",
                        "wicket",
                        "Maiden",
                        "4-wicket-haul",
                        "5-wicket-haul",
                    ]
                ) + sum(
                    self.bowling_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key
                    not in [
                        "match_id",
                        "runs",
                        "boundaries",
                        "sixes",
                        "100",
                        "50",
                        "duck",
                    ]
                )
            elif role == "wicket-keeper":
                player_scores[score_data["match_id"]] = sum(
                    self.batting_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key not in ["match_id", "Catch", "Stump"]
                ) + sum(
                    self.wk_dict[key][int(match_type) - 1] * int(score_data[key])
                    for key in score_data
                    if key
                    not in [
                        "match_id",
                        "runs",
                        "boundaries",
                        "sixes",
                        "100",
                        "50",
                        "duck",
                    ]
                )
        scores = [player_scores[k] for k in sorted(player_scores)]
        regr = LinearRegression(fit_intercept=True)
        y_train = np.array(scores).reshape(-1, 1)
        x_train = np.array(range(5)).reshape(-1, 1)
        try:
            regr.fit(x_train, y_train)
            pred = regr.predict(np.array(5).reshape(1, -1))
            if pred[0][0] < 0:
                result = 0
            else:
                result = pred[0][0]
        except ValueError:
            result = -1
        return result

    def get_min_team(self, players):
        """
        Gets the min team as per the fantasy league
        """
        role_score_map = {
            "batsman": sorted(
                [player for player in players if player["role"] == "batsman"],
                key=lambda i: i["score"],
            )[-3:],
            "bowler": sorted(
                [player for player in players if player["role"] == "bowler"],
                key=lambda i: i["score"],
            )[-3:],
            "all-rounder": sorted(
                [player for player in players if player["role"] == "all-rounder"],
                key=lambda i: i["score"],
                reverse=True,
            )[0:1],
            "wicket-keeper": sorted(
                [player for player in players if player["role"] == "wicket-keeper"],
                key=lambda i: i["score"],
                reverse=True,
            )[:1],
        }

        for role in role_score_map:
            for player in role_score_map[role]:
                if player["team"] == self.team1:
                    self.fantasy_team[self.team1].append(player)
                elif player["team"] == self.team2:
                    self.fantasy_team[self.team2].append(player)

        return self.fantasy_team[self.team1] + self.fantasy_team[self.team2]

    def fetch_fantasy_team(
        self, player_team1: List[str], player_team2: List[str], match_type: str
    ):
        """
        Builds the fantasy Team
        """
        players = self.espn.get_player_dets(player_team1, self.team1)
        players += self.espn.get_player_dets(player_team2, self.team2)
        remove = []
        for player in players:
            score_info = self.espn.get_match_det(
                player["player_id"], player["role"], match_type
            )
            if len(score_info) == 5:
                player["score"] = self.get_score(player["role"], match_type, score_info)
            else:
                remove.append(player)

        for player in remove:
            players.remove(player)

        remove = self.get_min_team(players)

        for player in remove:
            players.remove(player)

        for player in sorted(players, key=lambda i: i["score"]):
            if (
                len(self.fantasy_team[self.team1]) + len(self.fantasy_team[self.team2])
            ) == 11:
                break
            if player["team"] == self.team1:
                if len(self.fantasy_team[self.team1]) != 7:
                    self.fantasy_team[self.team1].append(player)
            elif player["team"] == self.team2:
                if len(self.fantasy_team[self.team2]) != 7:
                    self.fantasy_team[self.team2].append(player)
