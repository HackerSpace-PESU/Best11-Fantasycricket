"""
This module evaluates the performnce of the model
"""

from os import system, name
import os
import warnings
import pandas as pd
from tqdm import tqdm
from team import Teams
from team import Predict


# Remove all the warnings that show on console
warnings.filterwarnings("ignore")

# csv file containing the winning points for all 6 matches
winning_points = pd.read_csv("data/Winning points.csv")

values = {}

# Each ID maps to a specific match later used to calculate corresponding points
ID = ["a", "b", "c", "d", "e", "f"]


# define our clear function
def clear():
    """
    Clears the console screen
    """
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def get_my11score_wk(playername, match_id):
    """
    Returns My11 Wicket Keeping Score

        Parameters:
            playername (str): Player whose WK score will be calculated
            match_id (str): Match where the players score will be calculated

        Returns:
            wkscore (int): My11 WK score of the player of the given match
    """
    wk = pd.DataFrame()
    try:
        wk = pd.read_csv("data/wk/" + playername)
    except:
        wkscore = 0

    if not wk.empty:
        match_id = match_id.replace("@", "/")
        match_id = match_id.replace("p_", "p?")
        match_id = match_id.strip()

        wk = wk[wk["MATCH_ID"] == match_id]

        if not wk.empty:
            wkscore = float(wk.SCORE.values[0]) / 2
        else:
            wkscore = 0

    return wkscore


def get_my11score_ball(playername, match_id):
    """
    Returns My11 Bowling Score

        Parameters:
            playername (str): Player whose bowling score will be calculated
            match_id (str): Match where the players score will be calculated

        Returns:
            ballscore (int): My11 bowling score of the player of the given match
    """
    ball = pd.DataFrame()

    try:
        ball = pd.read_csv("data/bowl/" + playername)
    except:
        ballscore = 0

    if not ball.empty:
        match_id = match_id.replace("@", "/")
        match_id = match_id.replace("p_", "p?")
        match_id = match_id.strip()

        ball = ball[ball["Match_id"] == match_id]

        if not ball.empty:
            w = 12 * float(ball.Wicket.values[0])
            if float(ball.Wicket.values[0]) >= 7:
                w += 9
            elif float(ball.Wicket.values[0]) >= 5:
                w += 6
            elif float(ball.Wicket.values[0]) >= 3:
                w += 3
            o = float(ball.Overs.values[0])
            m = 4 * float(ball.Maidens.values[0])
            e = 0
            if o >= 2:
                if float(ball.Economy.values[0]) < 3:
                    e += 3
                elif float(ball.Economy.values[0]) <= 4.49:
                    e += 2
                elif float(ball.Economy.values[0]) <= 5.99:
                    e += 1
                elif float(ball.Economy.values[0]) <= 7.49:
                    e += 0
                elif float(ball.Economy.values[0]) <= 8.99:
                    e -= 1
                elif float(ball.Economy.values[0]) > 9:
                    e -= 2
            ballscore = w + m + e
        else:
            ballscore = 0

    return ballscore


def get_my11score_bat(playername, match_id):
    """
    Returns My11 Batting Score

        Parameters:
            playername (str): Player whose batting score will calculated
            match_id (str): Match where the players score will be calculated

        Returns:
            batscore (int): My11 batting score of the player of the given match
    """
    bat = pd.read_csv("data/zip2/" + playername)

    match_id = match_id.replace("@", "/")
    match_id = match_id.replace("p_", "p?")
    match_id = match_id.strip()

    bat = bat[bat["match_id"] == match_id]
    score = bat["score"].values[0]

    if score != "-":
        runs = float(score) - float(bat["4s"]) - (2 * float(bat["6s"]))
    elif score == "-":
        runs = 0

    if runs > 50:
        runs -= 4
    elif runs > 100:
        runs -= 8

    bat["runs"] = runs

    if score != "-":
        batscore = ((float(runs) * 0.5) + (float(bat["4s"]) * 0.5) + float(bat["6s"]))
    elif score == "-":
        batscore = 0

    if 50 <= runs <= 99:
        batscore += 2
    elif 100 <= runs <= 199:
        batscore += 4
    elif runs >= 200:
        batscore += 8

    return batscore


def main():
    for ids in ID:

        # Create an instance of the teams class to use its member functions
        t = Teams(ids)

        file_name = t.match
        """
        Returns the file name corresponding to the ID 'we'
        Format of file: {match}%{matchid}%{date}.csv
        """

        match, match_ID, date = (
            file_name.split("%")[0],
            file_name.split("%")[1],
            file_name.split("%")[2][:-4],
        )

        # Mapping from ID to match name
        matchname = t.get_match

        # Assigning the ID to the match name in the dictionary
        # matchname[we] = match

        # Dictionary which maps matches to the score obtained using the recommended team
        values[match] = {}

        # Returns the players recommended by the regression model
        captain, vc, wkteam, allteam, ballteam, batteam = t.team()
        players = t.player

        values[match][Predict.value] = None

        # Total score obtained from the given team
        teamtotal = 0

        for player in players:

            # batscore, ballscore, my11score = 0, 0, 0

            # Name of the player
            player_name = player[0:player.find("(")]

            player_name = player_name.strip()

            for i in tqdm(os.listdir("data/zip/")):
                if player_name in i:
                    player_name = i
                    break

            # Returns my11 batting score using my11 scoring scheme
            batscore = get_my11score_bat(player_name, match_ID)

            # Returns my11 bowling score using my11 scoring scheme
            ballscore = get_my11score_ball(player_name, match_ID)

            # Returns my11 WK score using my11 scoring scheme
            wkscore = get_my11score_wk(player_name, match_ID)

            # Calculate total score obtained
            total = batscore + ballscore + wkscore

            if player == captain:
                total = total * 2
            elif player == vc:
                total *= 1.5
            else:
                total = total

            teamtotal += total

        if ids == "a":
            values[match][Predict.value] = teamtotal + 18
        elif ids == "b":
            values[match][Predict.value] = teamtotal + 31
        elif ids == "c":
            values[match][Predict.value] = teamtotal + 30
        elif ids == "d":
            values[match][Predict.value] = teamtotal + 20
        elif ids == "e":
            values[match][Predict.value] = teamtotal + 11
        elif ids == "f":
            values[match][Predict.value] = teamtotal + 38

    loss = {}
    win = {}
    for i  in range(len(winning_points)):
        #print(matchname)
        print(i)
        print(winning_points.iloc[i,-1])
        match_id = matchname[winning_points.iloc[i, -1]].split("%")[0].strip()
        print(match_id)
        difference = winning_points.iloc[i, 1] - values[match_id][Predict.value]
        win[match_id] = winning_points.iloc[i, 1]
        loss[match_id] = difference

    clear()
    x = []
    for i in values:
        x.append([i, values[i][5], loss[i], win[i], str((100 * (loss[i] / win[i]))) + "%"])

    x = pd.DataFrame(
        x,
        columns=[
            "Game",
            "Real points Score",
            "Loss from Winning Score",
            "Winning Score",
            "loss percentage",
        ],
    )

    print(x.head(6))

main()
