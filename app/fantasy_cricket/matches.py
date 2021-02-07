"""
The module is defined to get upcoming match data of the next 2 days
"""

from typing import List
from app.fantasy_cricket.scrapyrt_client import EspnClient


class Matches:
    """
    A class to get upcoming live match data of the next 2 days

    """

    def __init__(self) -> None:

        self.espn = EspnClient()

    def get_upcoming_match(self):
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

    def get_squad_match_type(self, teams: List[str]):
        """
        Gets squad and match_class based on teams
        """

        for match in self.espn.get_upcoming_dets():

            if match["team1"] == teams[0] and match["team2"] == teams[1]:
                match_det = {
                    "team1_squad": match["team1_squad"],
                    "team2_squad": match["team2_squad"],
                    "match_type": match["match_id"],
                }
                break

        return match_det
