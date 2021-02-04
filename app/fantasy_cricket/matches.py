"""

The module is defined to get upcoming match data of the next 2 days

"""

import json
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict
from app.fantasy_cricket.ScrapyRTClient import espn_scrapyrt_client, Squad


class Match(TypedDict):
    team1: str
    team2: str
    flag_team1: str
    flag_team2: str


class Upcoming(TypedDict):

    team1_squad: Squad
    team2_squad: Squad
    match_type: str


class Matches:
    """
    A class to get upcoming live match data of the next 2 days

    """

    def __init__(self) -> None:

        self.espn = espn_scrapyrt_client()

    def get_upcoming_match(self) -> List[Match]:
        """
        Gets current matches dict
        """
        matches = []
        for match in self.espn.get_upcoming_dets():
            if match["team1_squad"] != [] and match["team2_squad"] != []:
                matches.append(
                    {
                        "team1": match["team1"],
                        "team2": match["team2"],
                        "flag_team1": "https://a.espncdn.com/i/teamlogos/cricket/500/"
                        + match["team1_id"]
                        + ".png",
                        "flag_team2": "https://a.espncdn.com/i/teamlogos/cricket/500/"
                        + match["team2_id"]
                        + ".png",
                    }
                )

        return matches

    def get_squad_match_type(self, teams: List[str]) -> Upcoming:
        """
        Gets squad file based on teams
        """

        for match in self.espn.get_upcoming_dets():

            if match["team1"] == teams[0] and match["team2"] == teams[1]:
                return {
                    "team1_squad": match["team1_squad"],
                    "team2_squad": match["team2_squad"],
                    "match_type": match["match_id"],
                }
