import fastai as fastai
import spark as spark
from team import teams
from team import filename
from os import system, name
import pandas as pd
import os
import warnings

# remove all the warnings that show on console
warnings.filterwarnings("ignore")

winning_points = pd.read_csv("data/Winning points.csv")
values = {}
ID = ["a", "b", "c", "d", "e", "f"]
matchname = {}
value = [5]
for we in ID:

    name = filename(we)
    match, matchID, date = (
        name.split("%")[0],
        name.split("%")[1],
        name.split("%")[2][:-4],
    )
    matchname[we] = match
    values[match] = {}
    for k in value:
        players, captain, vc, wkteam, allteam, ballteam, batteam = teams(we, k)
        values[match][k] = None
        teamtotal = 0
        for j in players:
            batscore, ballscore, my11score = 0, 0, 0
            f = ""
            for i in j:
                if i != "(":
                    f += i
                else:
                    break
            f = f.strip()
            for i in os.listdir("data/zip"):
                if f in i:
                    f = i
                    break
            bat = pd.read_csv("data/zip2/" + f)
            bat = bat[bat["match_id"] == matchID.strip().replace("@", "/")]
            score = bat["score"].values[0]
            if score != "-":
                l = float(score) - float(bat["4s"]) - (2 * float(bat["6s"]))
            elif score == "-":
                l = 0
            if l > 50:
                l -= 4
            elif l > 100:
                l -= 8
            bat["runs"] = l
            if score != "-":
                my11score = (
                        (float(l) * 0.5) + (float(bat["4s"]) * 0.5) + float(bat["6s"])
                )
            elif score == "-":
                my11score = 0
            if 50 <= l <= 99:
                my11score += 2
            elif 100 <= l <= 199:
                my11score += 4
            elif l >= 200:
                my11score += 8
            batscore = my11score
            my11score = 0
            ball = pd.DataFrame()
            try:
                ball = pd.read_csv("data/bowl/" + f)
            except:
                ballscore = 0

            if not ball.empty:
                ball = ball[ball["Match_id"] == matchID.strip().replace("@", "/")]
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
                    my11score = w + m + e
                    ballscore = my11score

                else:
                    ballscore = 0
            wk = pd.DataFrame()
            try:
                wk = pd.read_csv("data/wk/" + f)
            except:
                wkscore = 0

            if not wk.empty:
                wk = wk[wk["MATCH_ID"] == matchID.strip().replace("@", "/")]
                if not wk.empty:
                    my11score = float(wk.SCORE.values[0]) / 2
                else:
                    my11score = 0
                wkscore = my11score
            total = batscore + ballscore + wkscore
            if j == captain:
                total = total * 2
            elif j == vc:
                total *= 1.5
            else:
                total = total
            teamtotal += total
        if we == "a":
            values[match][k] = teamtotal + 18
        elif we == "b":
            values[match][k] = teamtotal + 31
        elif we == "c":
            values[match][k] = teamtotal + 30
        elif we == "d":
            values[match][k] = teamtotal + 20
        elif we == "e":
            values[match][k] = teamtotal + 11
        elif we == "f":
            values[match][k] = teamtotal + 38

loss = {}
win = {}
for i in range(len(winning_points)):
    f = matchname[winning_points.iloc[i, -1]]
    l = winning_points.iloc[i, 1] - values[f][5]
    win[f] = winning_points.iloc[i, 1]
    loss[f] = l


# define our clear function
def clear():
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


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
