"""
This module defines the teams class which outputs the team for the match
and the Predict class which predicts the score based on the role
"""

import pandas as pd
import numpy as np
import os
from collections import Counter
from sklearn.linear_model import LinearRegression

class teams(object):
    """A team class which is defined as a base in predicting teams
    
    * **get_match** : a dictionary which maps the Id of the selected match 
                      to the match name 
    * **Id**: Id of the match chosen by the user
    * **match**: Match name of the selected Id
    * **team_dict**: dictionary which maps the team name to count of the players 
                     selected from that team
    *param Id: Id passed to select team for a match
    """

    get_match = {
                    "a":"England vs Australia SemiFinal",
                    "b": "England vs Australia",
                    "c": "Bangladesh vs India",
                    "d": "England vs India",
                    "e": "Australia vs India",
                    "f": "India vs New Zealand",
                }
    
    def __init__(self,Id):
        self.Id = Id
        self.match = self.get_match[self.Id]
        self.team_dict = {   
                            self.match.split("vs")[0].strip(): 0,
                            self.match.split("vs")[1].strip().split("Semi")[0].strip(): 0 ,      
                         }

    def filename(self):
        """
        Returns the file name corresponding to the Id 
        Each file can be found in data/6 Matches (Final)
        :rtype str
        """

        if self.Id == "a":
            return "EnglandvsAustraliaSemi%Matches@MatchScorecard_ODI.asp?MatchCode=4354%2019-07-11.csv"
        elif self.Id == "b":
            return "EnglandvsAustralia%Matches@MatchScorecard_ODI.asp?MatchCode=4336%2019-06-25.csv"
        elif self.Id == "c":
            return "Bangladesh vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4345%2019-07-02.csv"
        elif self.Id == "d":
            return "England vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4342%2019-06-30.csv"
        elif self.Id == "e":
            return "Australia vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4316%2019-06-09.csv"
        elif self.Id == "f":
            return "India vs New Zealand%Matches@MatchScorecard_ODI.asp?MatchCode=4353%2019-07-09.csv"

    def get_role_team(self,role, role_data, file_name):
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

        for player_det in role_data.name:
            if player_det.split("-")[0] not in team:
                team[player_det.split("-")[0]] = None
            team[player_det.split("-")[0]] = Predict(player_det.split("-")[0], 
                                                                role, 
                                                                file_name.split("%")[2][:-4]).result
        wkt = sorted(team.items(), key=lambda x: x[1], reverse=True)
        wkteam = {i[0]: i[1] for i in wkt}
        return wkteam

    def get_max_players(self,role_dict,player,role):
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
        max_score = { 
                        "wk": [max(role_dict , key = role_dict.get)],
                        "all": [max(role_dict , key = role_dict.get)],
                        "bat": list(zip(*Counter(role_dict).most_common(3)))[0],
                        "ball": list(zip(*Counter(role_dict).most_common(3)))[0],
                    }
        names = max_score[role]
        for name in names:
            if list(self.team_dict.keys())[0] in name:
                self.team_dict[list(self.team_dict.keys())[0]]+=1
            elif list(self.team_dict.keys())[1] in name:
                self.team_dict[list(self.team_dict.keys())[1]]+=1
            elif "Nathan" in name:
                if list(self.team_dict.keys())[0] == "Australia":
                    self.team_dict[list(self.team_dict.keys())[0]]+=1
                elif list(self.team_dict.keys())[1] == "Australia":
                    self.team_dict[list(self.team_dict.keys())[1]]+= 1
            if name not in player:
                player[name] = role_dict[name]
        return player
    
    def get_restofteam(self,role_dict,player,reduntant,restteam):
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
            if i not in player and i not in reduntant:
                restteam[i] = role_dict[i]
        return restteam
    
    def get_captain(self,player):
        """
        Returns Captain and Vice Captain for the selected 11
        :param player: dictionary of the selected players for the best11
        :type dict( str : float)
        :rtype: tuple(str,str)
        """
        captains = list(zip(*Counter(player).most_common(2)))
        captain ,vcaptain = captains[0][0],captains[0][1]
        return captain ,vcaptain
    
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

        player = {}
        name=self.filename()
        files = pd.read_csv("data/6 Matches (Final)/" + name , encoding = "utf-8")
        wkteam = batteam = ballteam = allteam = None
        position_map = {
                            "wk": {"var" : wkteam}, 
                            "bat": { "var" : batteam}, 
                            "ball": {"var" : ballteam},
                            "all": {"var" : allteam},
                       }
        for role in position_map.keys():
            role_data = files[files["role"] == role]
            position_map[role]["var"] = self.get_role_team(role,role_data,name)
            player = self.get_max_players(position_map[role]["var"] , player , role)
        count = 0
        rm = []
        while count < 3:
            restteam = {}
            for role in position_map.keys():
                restteam = self.get_restofteam(position_map[role]["var"],player,rm,restteam)
            new = max(restteam , key = restteam.get)
            if list(self.team_dict.keys())[0] in new:
                if self.team_dict[list(self.team_dict.keys())[0]] < 7:
                    player[new] = restteam[new]
                    count += 1
                    self.team_dict[list(self.team_dict.keys())[0]]+=1
                else:
                    rm.append(new)
            elif list(self.team_dict.keys())[1] in new:
                if self.team_dict[list(self.team_dict.keys())[1]] < 7:
                    player[new] = restteam[new]
                    count += 1
                    self.team_dict[list(self.team_dict.keys())[1]]+=1
                else:
                    rm.append(new)
            elif "Nathan" in new:
                if list(self.team_dict.keys())[0] == "Australia":
                    if self.team_dict[list(self.team_dict.keys())[0]]< 7:
                        player[new] = restteam[new]
                        count += 1
                        self.team_dict[list(self.team_dict.keys())[0]]+= 1
                    else:
                        rm.append(new)
                elif list(self.team_dict.keys())[1] == "Australia":
                    if self.team_dict[list(self.team_dict.keys())[1]] < 7:
                        player[new] = restteam[i]
                        self.team_dict[list(self.team_dict.keys())[1]]+= 1
                        count += 1
                    else:
                        rm.append(new)
        captain,vcaptain = self.get_captain(player)
        return player, captain, vcaptain, wkteam, allteam, ballteam, batteam

class Predict(object):
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
    
    value =5
    
    def __init__(self,player,role,date):
        self.get_filename(player)
        self.date = date
        predict_map = {
            "all": self.predict_allrounder,
            "wk" : self.predict_wk,
            "bat": self.predict_bat,
            "ball": self.predict_ball,
        }
        self.dates =pd.read_csv("data/zip/ODI/" + self.player_name)
        self.result = predict_map[role]()

    def get_filename(self,player):
        """
        Returns filename corresponding to the player
        (to be removed soon)
        
        :rtype : void
        """

        self.player_name = player.split('(')[0].strip()
        for i in os.listdir("data/zip/ODI/"):
            if self.player_name in i:
                self.player_name = i
                break

    def predict(self, scores):
        """
        Returns the predicted score 
        :param : scores : A numpy array with the scores of all matches the 
                          player has played
        :type : numpy.array()
        :rtype : float
        """

        regr = LinearRegression(fit_intercept=True)
        y_train = np.array(scores[len(scores) - self.value:]).reshape(-1, 1)
        X_train = np.array(range(self.value)).reshape(-1, 1)
        try:
            regr.fit(X_train, y_train)
        except ValueError:
            return -1
        pred = regr.predict(np.array(self.value).reshape(1, -1))
        if pred[0][0] < 0:
            return 0
        else:
            return pred[0][0]

    def predict_allrounder(self):
        """
        Returns the predicted score for the coresponding match for all rounders
        
        :rtype : float
        """

        batting_score = pd.read_csv("data/zip2/ODI/" + self.player_name)
        bowling_score = pd.read_csv("data/bowl/ODI/" + self.player_name)
        scores = batting_score.merge(
            bowling_score, how="left", left_on="match_id", right_on="Match_id"
        )
        scores = self.dates.merge(scores, how="left", left_on="matchid", right_on="match_id")

        scores = scores.sort_values(by="date", ascending=True).reset_index(drop=True)
        x = scores[scores["date"] == self.date].index.to_list()[0]
        scores = scores.iloc[0:x, :]
        scores.drop([
                        "Match_id",
                        "how dismissed",
                        "Wicket",
                        "Economy",
                        "Maidens",
                        "Unnamed: 0",
                        "batting position",
                        "6s",
                        "4s",
                        "strike rate",
                        "match_id",
                        "date",
                    ],
                    axis=1,
                    inplace=True,
                )

        scores["score"] = scores["score"].apply(lambda x: 0 if x == "-" else x)
        scores["score"] = scores["score"].apply(pd.to_numeric)
        scores["Score"] = scores["Score"].apply(pd.to_numeric)

        scores["Total"] = scores["score"] + scores["Score"]
        scores.dropna(inplace=True)
        scores = scores[["Total"]]

        result = self.predict(scores[["Total"]].values)
        return result

    def predict_wk(self):
        """
        Returns the predicted score for the coresponding match for wicket-keepers
        
        :rtype : float
        """

        wk_score = pd.read_csv("data/wk/ODI/" + self.player_name)
        batting_score = pd.read_csv("data/zip2/ODI/" + self.player_name)
        scores = batting_score.merge(
            wk_score, how="left", left_on="match_id", right_on="MATCH_ID"
        )
        scores = self.dates.merge(scores, how="left", left_on="matchid", right_on="match_id")
        scores = scores.sort_values(by="date", ascending=True).reset_index(drop=True)
        x = scores[scores["date"] == self.date].index.to_list()[0]
        scores = scores.iloc[0:x, :]
        scores.dropna(inplace=True)
        scores.drop(
            [
                "match_id",
                "MATCH_ID",
                "how dismissed",
                "Unnamed: 0",
                "batting position",
                "6s",
                "4s",
                "strike rate",
                "date",
            ],
            axis=1,
            inplace=True,
        )

        scores["score"] = scores["score"].apply(lambda x: 0 if x == "-" else x)
        scores["score"] = scores["score"].apply(pd.to_numeric)
        scores["SCORE"] = scores["SCORE"].apply(pd.to_numeric)

        scores["Total"] = scores["score"] + scores["SCORE"]
        scores.dropna(inplace=True)
        scores = scores[["Total"]]
        result = self.predict(scores[["Total"]].values)
        return result

    def predict_bat(self):
        """
        Returns the predicted score for the coresponding match for batsmen
        
        :rtype : float
        """

        batting_score = pd.read_csv("data/zip2/ODI/" + self.player_name)
        scores = self.dates.merge(batting_score, how="left", left_on="matchid", right_on="match_id")
        scores = scores.sort_values(by="date", ascending=True).reset_index(drop=True)
        x = scores[scores["date"] == self.date].index.to_list()[0]
        scores = scores.iloc[0:x, :]
        scores.drop(
            ["strike rate", "4s", "6s", "how dismissed", "batting position", "matchid"],
            axis=1,
            inplace=True,
        )
        scores.dropna(inplace=True)
        scores = scores[scores["score"] != "-"]
        result = self.predict(scores["score"].values)
        return result

    def predict_ball(self):
        """
        Returns the predicted score for the corresponding match for bowlers
        :rtype : float
        """

        bowling_score = pd.read_csv("data/bowl/ODI/" + self.player_name)
        scores = self.dates.merge(bowling_score, how="left", left_on="matchid", right_on="Match_id")
        scores = scores.sort_values(by="date", ascending=True).reset_index(drop=True)
        x = scores[scores["date"] == self.date].index.to_list()[0]
        scores = scores.iloc[0:x, :]
        scores.drop(["Economy", "Wicket", "Maidens"], axis=1, inplace=True)
        scores.dropna(inplace=True)
        result = self.predict(scores["Score"].values)
        return result

