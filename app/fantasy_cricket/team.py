"""
This module defines the teams class which outputs the team for the match
and the Predict class which predicts the score based on the role
Copyright (C) 2020  Royston E Tauro & Sammith S Bharadwaj & Shreyas Raviprasad
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import Counter
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class Teams:
    """A team class which is defined as a base in predicting teams
    * **get_match** : a dictionary which maps the match_id of the selected match
                      to the match name
    * **match_id**: match_id of the match chosen by the user
    * **match**: Match name of the selected match_id
    * **team_dict**: dictionary which maps the team name to count of the players
                     selected from that team
    *param Id: Id passed to select team for a match
    """

    def __init__(self, path):
        self.path = path
        self.team_dict = {}
        self.player = {}
        self.data = {}

    def get_max_players(self, role_dict, role):
        """
        Returns max player for a particular role
        :param role_dict : dict of the players mapped to the score for that role
        :type dict( str : float)
        :param player : dictionary of the selected players for the best11
        :type dict( str: float)
        :param role : role of the player
        :type str
        :rtype: dict( str: float)
        """
        if role_dict!={}:
            max_score = {
                "wk": [list(role_dict.keys())[0]],
                "all": [list(role_dict.keys())[0]],
                "bat": [key for key in role_dict][:3],
                "bowl": [key for key in role_dict][:3],
            }

            names = max_score[role]
            for name in names:
                if list(self.team_dict.keys())[0] in role_dict[name]["team"]:
                    self.team_dict[list(self.team_dict.keys())[0]] += 1
                elif list(self.team_dict.keys())[1] in role_dict[name]["team"]:
                    self.team_dict[list(self.team_dict.keys())[1]] += 1
                if name not in self.player:
                    self.player[name] = role_dict[name]

    def get_restofteam(self, role_dict, reduntant, restteam):
        """
        Returns the rest of the players who have not yet been chosen for the 11
        :param role_dict : dict of the players mapped to the score for that role
        :type dict( str : float)
        :param player : dictionary of the selected players for the best11
        :type dict( str: float)
        :param redundant : selected players
        :type list(str)
        :param restteam: dict of the players left to be selected
        :type dict( str: float)
        :rtype dict( str: float)
        """
        for i in role_dict:
            if i not in self.player and i not in reduntant:
                restteam[i] = role_dict[i]
                
        restteam = sorted(restteam.items(), key=lambda x: x[1]["score"], reverse=True)
        restteam = {i[0]: i[1] for i in restteam}
        return restteam

    def get_captain(self):
        """
        Returns Captain and Vice Captain for the selected 11
        :param player: dictionary of the selected players for the best11
        :type dict( str : float)
        :rtype: tuple(str,str)
        """
        self.player = [ i[0] for i in sorted(self.player.items(), key=lambda x: x[1]["score"], reverse=True)]
        captain, vcaptain = self.player[0], self.player[1]
        return captain, vcaptain

    def team(self):
        """
        Returns Captain,Vicecaptain and teams for each role
        :rtype: tuple(
                    str,
                    str,
                    dict( str : float),
                    dict( str : float),
                    dict( str : float),
                    dict( str : float),
                )
        """

        file_handler = open(self.path)
        self.data = json.load(file_handler)
        wkteam = batteam = ballteam = allteam = None
        position_map = {
            "wk": {"var": wkteam},
            "bat": {"var": batteam},
            "bowl": {"var": ballteam},
            "all": {"var": allteam},
        }
        for role in position_map:
            role_data = dict()
            for player in self.data.keys():
                if self.data[player]["team"] not in self.team_dict.keys():
                    self.team_dict[self.data[player]["team"]] = 0
                if self.data[player]["role"] == role:
                    role_data[player] = self.data[player]
            position_map[role]["var"] = get_role_team(role, role_data)
            self.get_max_players(position_map[role]["var"], role)
        
        count = 0
        redundant = []
        #print(position_map,self.team_dict)
        maxi = len(self.player)
        while count < 11-maxi:
            print(count)
            restteam = {}
            for role in position_map:
                restteam = self.get_restofteam(
                    position_map[role]["var"], redundant, restteam
                )
            new = list(restteam.keys())[0]
            if list(self.team_dict.keys())[0] in restteam[new]["team"]:
                if self.team_dict[list(self.team_dict.keys())[0]] < 7:
                    self.player[new] = restteam[new]
                    count += 1
                    self.team_dict[list(self.team_dict.keys())[0]] += 1
                else:
                    redundant.append(new)
            elif list(self.team_dict.keys())[1] in restteam[new]["team"]:
                if self.team_dict[list(self.team_dict.keys())[1]] < 7:
                    self.player[new] = restteam[new]
                    count += 1
                    self.team_dict[list(self.team_dict.keys())[1]] += 1
                else:
                    redundant.append(new)
        #print(self.player)
        captain, vcaptain = self.get_captain()
        return captain, vcaptain


class Predict:
    """
    A Predict class which predicts the score of the teams
    * **value** : Number of matches to consider so as to predict the next match score
    * **date**  : Date the match to be predicted is going to be played
    * **dates** : Dataframe of dates of all matches played by the player
          :type : pandas.DataFrame()
    * **result**: predicted score
    * **player_name** : file name corresponding to the player name
    :param : player : player name
    :type : str
    :param : role : player role
    :type : str
    :param : date : Date of the match
    : type : str
    """

    value = 5

    def __init__(self, player, data):
        scores = data[player]["scores"]
        scores = sorted(scores.items(), key = lambda x: x[0])
        scores = [i[1] for i in scores]
        self.result = self.predict(scores)

    def predict(self, scores):
        """
        Returns the predicted score
        :param : scores : A numpy array with the scores of all matches the
                          player has played
        :type : numpy.array()
        :rtype : float
        """

        regr = LinearRegression(fit_intercept=True)
        y_train = np.array(scores[len(scores) - self.value :]).reshape(-1, 1)
        x_train = np.array(range(self.value)).reshape(-1, 1)
        try:
            regr.fit(x_train, y_train)
            pred = regr.predict(np.array(self.value).reshape(1, -1))
            if pred[0][0] < 0:
                result = 0
            else:
                result = pred[0][0]
        except ValueError:
            result = -1
        return result


def get_role_team(role, data):
    """
    Returns the player names and score corresponding to a role
    from the files dataframe
    :param role : role of the players in the dataframe
    :type str
    :param role_data : dataframe of the list of players and files
    :type pandas.DataFrame()
    :param file_name : file name of the match
    :type str
    :rtype: dict(str: float)
    """

    team = {}

    for player_det in data.keys():
        if player_det not in team:
            team[player_det] = {}
        team[player_det]["score"] = Predict(player_det, data).result
        team[player_det]["team"] = data[player_det]["team"]
    wkt = sorted(team.items(), key=lambda x: x[1]["score"], reverse=True)
    wkteam = {i[0]: i[1] for i in wkt}

    return wkteam
