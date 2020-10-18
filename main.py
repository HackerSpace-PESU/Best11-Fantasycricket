"""
Module which runs the GUI for the project using FastAPI
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from team import Teams

# pylint: disable=missing-function-docstring
# pylint: disable=global-variable-undefined

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def home_post(match: str = Form(...)):
    global MATCH_ID
    MATCH_ID = match
    response = RedirectResponse(url="/results")
    return response


@app.post("/results", response_class=HTMLResponse)
def result(request: Request):
    t_d = Teams(MATCH_ID)
    team_match = t_d.team()
    vcaptain = team_match[1]
    captain = team_match[0]
    team_list = t_d.player
    players = []
    captain_tag= {
        captain:"(C)",
        vcaptain:"(VC)"
    }
    for i in team_list:
        try:
            tag_c = captain_tag[i]
        except KeyError:
            tag_c = ""
        if i == "Nathan Coulter":
            players.append("Nathan Coulter Nile" + tag_c)
        elif "Eoin Morgan" in i:
            players.append("Eoin Morgan" + tag_c)
        elif "Jason Roy" in i:
            players.append("Jason Roy" + tag_c)
        elif "Liam Plunkett" in i:
            players.append("Liam Plunkett" + tag_c)
        else:
            players.append(i[: i.find("\xa0")] + tag_c)
    captain_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vcaptain_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i, _ in enumerate(players):
        if "(C)" in players[i]:
            captain_list[i] = "(C)"
            vcaptain_list[i] = ""
            players[i] = players[i][:-3]
        elif "(VC)" in players[i]:
            vcaptain_list[i] = "(VC)"
            captain_list[i] = ""
            players[i] = players[i][:-4]
        else:
            vcaptain_list[i] = ""
            captain_list[i] = ""
    return templates.TemplateResponse(
        "result.html",
        context={
            "request": request,
            "c1": captain_list[0],
            "v1": vcaptain_list[0],
            "t1": players[0],
            "c2": captain_list[1],
            "v2": vcaptain_list[1],
            "t2": players[1],
            "c3": captain_list[2],
            "v3": vcaptain_list[2],
            "t3": players[2],
            "c4": captain_list[3],
            "v4": vcaptain_list[3],
            "t4": players[3],
            "c5": captain_list[4],
            "v5": vcaptain_list[4],
            "t5": players[4],
            "c6": captain_list[5],
            "v6": vcaptain_list[5],
            "t6": players[5],
            "c7": captain_list[6],
            "v7": vcaptain_list[6],
            "t7": players[6],
            "c8": captain_list[7],
            "v8": vcaptain_list[7],
            "t8": players[7],
            "c9": captain_list[8],
            "v9": vcaptain_list[8],
            "t9": players[8],
            "c10": captain_list[9],
            "v10": vcaptain_list[9],
            "t10": players[9],
            "c11": captain_list[10],
            "v11": vcaptain_list[10],
            "t11": players[10],
        },
    )
