"""
Module which helps to get current match data
Copyright (C) 2020  Royston E Tauro & Sammith S Bharadwaj & Shreyas Raviprasad

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
-
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
from pycricbuzz import Cricbuzz


class Matches:
    """
    Class which gets and parses matches within 24 hours period
    """

    def __init__(self):
        """
        cricket: class of cricbuzz
        supported teams: supported teams by our module
        flags: flags json with links
        """

        self.cricket = Cricbuzz().matches()

        self.supported_teams = [
            "India",
            "Australia",
            "New Zealand",
            "England",
            "Bangladesh",
            "South Africa",
            "West Indies",
            "Pakistan",
            "Afghanistan",
            "Sri Lanka",
        ]
        with open("./app/fantasy_cricket/data/flags.json") as flag_file:
            self.flags = json.load(flag_file)

    def get_match(self):
        """
        Gets current matches dict
        """
        matches = []
        for match in self.cricket:

            if (
                match["team1"]["name"] in self.supported_teams
                and match["team2"]["name"] in self.supported_teams
                # and match["mchstate"] == "preview"
            ):
                matches.append(
                    (
                        match["team1"],
                        match["team2"],
                        self.flags["countries"][match["team1"]["name"]],
                        self.flags["countries"][match["team2"]["name"]],
                    )
                )
        return matches

    def get_squad_file_match_type(self, teams):

        for match in self.cricket:

            if (
                match["team1"]["name"] == teams[0]
                and match["team2"]["name"] == teams[1]
            ):
                return (
                    match["team1"]["squad_bench"] + match["team1"]["squad"],
                    match["team2"]["squad_bench"] + match["team2"]["squad"],
                    match["srs"] + match["mnum"], 
                    match["type"]
                )
                # return [match["team1"]["squad_bench"], match["team2"]["squad_bench"]]

    def get_file_name_and_type(self, teams):
        for match in self.cricket:

            if (
                match["team1"]["name"] == teams[0]
                and match["team2"]["name"] == teams[1]
            ):
                return (match["srs"] + match["mnum"], match["type"])
