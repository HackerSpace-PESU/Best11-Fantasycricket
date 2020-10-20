"""
This module evaluates the performnce of the model
"""

import bisect
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
    if os.name == "nt":
        _ = os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system("clear")

def get_dataframe(filename,player):
    """
    Returns the data frame corresponding to the player

    :param filename : filename of the role of the player
    :type : str
    :param player : player name
    :type : str

    :rtype: :pyclass: `pd.DataFrame()`
    """
    data = pd.read_csv('data/ODI/'+filename)
    data = data[data['player_name']==player]
    if data.empty:
        index =[]
        data = pd.read_csv('data/ODI/'+filename)
        for i,_ in enumerate(data.iloc[:,-1].values):
            if player.split('(')[0].strip() in data.iloc[i,-1]:
                index.append(i)
        data = data.iloc[index,:-1]
    return data

def get_my11score_wk(playername, match_id):
    """
    Returns My11 Wicket Keeping Score

        Parameters:
            playername (str): Player whose WK score will be calculated
            match_id (str): Match where the players score will be calculated

        Returns:
            wkscore (int): My11 WK score of the player of the given match
    """
    wkscore = 0
    wicket_keeper = pd.DataFrame()
    wicket_keeper = get_dataframe("wicketkeeping_ODI.csv", playername)

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
    ballscore = 0
    ball = get_dataframe("bowling_ODI.csv", playername)

    if not ball.empty:
        match_id = match_id.replace("@", "/").replace("p_", "p?").strip()

        ball = ball[ball["Match_id"] == match_id]

        if not ball.empty:
            wicket = 12 * float(ball.Wicket.values[0])
            #if-else statement alternative
            i = bisect.bisect([2,4,6,10],float(ball.Wicket.values[0])-1)
            wicket += int("0369"[i])
            over = float(ball.Overs.values[0])
            maiden = 4 * float(ball.Maidens.values[0])
            economy = 0
            if over >= 2:
                i = bisect.bisect([3,4.49,5.99,7.49,8.99,float('inf')],\
                    float(ball.Economy.values[0]))
                economy+=[3,2,1,0,-1,-2][i]
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
    bat = get_dataframe("batting_ODI.csv", playername)

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
        print(ids)
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

            # Calculate total score obtained
            total = (
                get_my11score_bat(player, team_class.match.split("%")[1])
                + get_my11score_ball(player, team_class.match.split("%")[1])
                + get_my11score_wk(player, team_class.match.split("%")[1])
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
