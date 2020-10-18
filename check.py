"""
This module evaluates the performnce of the model
"""

from os import system, name
import os
import warnings
import pandas as pd
from team import Teams, Predict



# csv file containing the winning points for all 6 matches
winning_points = pd.read_csv("data/Winning points.csv")

scores = {}

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
    wicket_keeper = pd.DataFrame()
    try:
        wicket_keeper = pd.read_csv("data/wk/ODI/" + playername)
    except FileNotFoundError:
        wkscore = 0

    if not wicket_keeper.empty:
        match_id = match_id.replace("@", "/").replace("p_", "p?").strip()
        wicket_keeper = wicket_keeper[wicket_keeper["MATCH_ID"] == match_id]

        if not wicket_keeper.empty:
            wkscore = float(wicket_keeper.SCORE.values[0]) / 2
        else:
            wkscore = 0

    return wkscore


def get_my11score_ball(playername, match_id):
    """Returns My11 Bowling Score

    Parameters:
        playername (str): Player whose bowling score will be calculated
        match_id (str): Match where the players score will be calculated

    Returns:
        ballscore (int): My11 bowling score of the player of the given match
    """
    # Remove all the warnings that show on console
    warnings.filterwarnings("ignore")

    ball = pd.DataFrame()

    try:
        ball = pd.read_csv("data/bowl/ODI/" + playername)
    except FileNotFoundError:
        ballscore = 0

    if not ball.empty:
        match_id = match_id.replace("@", "/").replace("p_", "p?").strip()

        ball = ball[ball["Match_id"] == match_id]

        if not ball.empty:
            wicket = 12 * float(ball.Wicket.values[0])
            if float(ball.Wicket.values[0]) >= 7:
                wicket += 9
            elif float(ball.Wicket.values[0]) >= 5:
                wicket += 6
            elif float(ball.Wicket.values[0]) >= 3:
                wicket += 3
            over = float(ball.Overs.values[0])
            maiden = 4 * float(ball.Maidens.values[0])
            economy = 0
            if over >= 2:
                if float(ball.Economy.values[0]) < 3:
                    economy += 3
                elif float(ball.Economy.values[0]) <= 4.49:
                    economy += 2
                elif float(ball.Economy.values[0]) <= 5.99:
                    economy += 1
                elif float(ball.Economy.values[0]) <= 7.49:
                    economy += 0
                elif float(ball.Economy.values[0]) <= 8.99:
                    economy -= 1
                elif float(ball.Economy.values[0]) > 9:
                    economy -= 2
            ballscore = wicket + maiden + economy
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
    bat = pd.read_csv("data/zip2/ODI/" + playername)

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
        batscore = (float(runs) * 0.5) + (float(bat["4s"]) * 0.5) + float(bat["6s"])
    elif score == "-":
        batscore = 0

    if 50 <= runs <= 99:
        batscore += 2
    elif 100 <= runs <= 199:
        batscore += 4
    elif runs >= 200:
        batscore += 8

    return batscore


fielding_points = {
    "a": 18,
    "b": 30,
    "c": 31,
    "d": 20,
    "e": 11,
    "f": 38,
}


def main():
    """Runs the check algorithm"""
    for ids in Teams.get_match:

        # Create an instance of the teams class to use its member functions
        team_class = Teams(ids)

        # Dictionary which maps matches to the score obtained using the recommended team
        scores[team_class.match.split("%")[0]] = {}

        # Returns the players recommended by the regression model
        captain, vcaptain = team_class.team()

        scores[team_class.match.split("%")[0]][Predict.value] = None

        # Total score obtained from the given team
        teamtotal = 0

        for player in team_class.player:

            # Name of the player

            for i in os.listdir("data/zip/ODI/"):
                if player[0 : player.find("(")].strip() in i:
                    player_name = i
                    break

            # Calculate total score obtained
            total = (
                get_my11score_bat(player_name, team_class.match.split("%")[1])
                + get_my11score_ball(player_name, team_class.match.split("%")[1])
                + get_my11score_wk(player_name, team_class.match.split("%")[1])
            )

            if player == captain:
                total *= 2
            elif player == vcaptain:
                total *= 1.5

            teamtotal += total

        scores[team_class.match.split("%")[0]][Predict.value] = (
            fielding_points[ids] + teamtotal
        )

    loss = {}
    win = {}
    for i in range(len(winning_points)):
        win[
            team_class.get_match[winning_points.iloc[i, -1]].split("%")[0].strip()
        ] = winning_points.iloc[i, 1]
        loss[team_class.get_match[winning_points.iloc[i, -1]].split("%")[0].strip()] = (
            winning_points.iloc[i, 1]
            - scores[
                team_class.get_match[winning_points.iloc[i, -1]].split("%")[0].strip()
            ][Predict.value]
        )

    result = []
    for i in scores:
        result.append(
            [i, scores[i][5], loss[i], win[i], str((100 * (loss[i] / win[i]))) + "%"]
        )

    result = pd.DataFrame(
        result,
        columns=[
            "Game",
            "Real points Score",
            "Loss from Winning Score",
            "Winning Score",
            "loss percentage",
        ],
    )

    return result

if __name__=="__main__":
    clear()
    checks = main()
    print(checks.head(6))
