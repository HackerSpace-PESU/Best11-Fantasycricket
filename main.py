"""
Module which runs the GUI for the project using FastAPI
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

import time
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form, Request, status, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fantasy_cricket.team import Teams
from fantasy_cricket.utils import Matches
from crawler.spiders.howstat import HowstatSpider

# pylint: disable=missing-function-docstring
# pylint: disable=global-variable-undefined

app = FastAPI()

templates = Jinja2Templates(directory="fantasy_cricket/templates")
app.mount("/static", StaticFiles(directory="fantasy_cricket/static"), name="static")


cricket = Matches()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    matches = cricket.get_match()
    teams = [
        [match[0]["name"], match[1]["name"], match[2]["flag"], match[3]["flag"]]
        for match in matches
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "teams": teams}
    )


@app.post("/")
async def home_post(match: str = Form(...)):
    response = RedirectResponse(
        url="/playing11?team1="
        + match.split(" vs ")[0]
        + "&team2="
        + match.split(" vs ")[-1],
        status_code=status.HTTP_302_FOUND,
    )
    return response


@app.get("/playing11", response_class=HTMLResponse)
def playing_11(team1,team2):

    squad1,squad2,file,match_type = cricket.get_squad_file_match_type(
        [team1,team2]
    )
    if os.path.isfile("data/"+file):
        timeout = 13
    else:
        timeout = 75
    return templates.TemplateResponse(
        "Playing_11.html",
        {
            "request": request,
            "squads": [squad1,squad2],
            "file": file,
            "match_type": match_type,
            "teams": [team1, team2],
        },
    )


@app.post("/playing11")
async def playing_11_post(request:Request,file,type,team1,team2,background_tasks: BackgroundTasks):
    playing_11 = list(jsonable_encoder(await request.form()).keys())
    playing_11.remove("Confirm")
    players1 = '"' + '","'.join(playing_11[0:11]) + '"'
    players2 = '"' + '","'.join(playing_11[11:]) + '"'
    
    background_tasks.add_task(
        scrape_with_crochet,
        file = file,
        match_type = file,
        team1 =file,
        team2 = file,
        players2 = players2,
        players1 = players1
    )
    
    return RedirectResponse(
        url = "/results?file="+file, 
        
    )


@app.post("/results", response_class=HTMLResponse)
def result(request: Request):
    if os.path.isfile("fantasy_cricket/data/"+file+".json"):
        timeout = 15
    else:
        timeout = 80
    time.sleep(timeout)
    t_d = Teams("fantasy_cricket/data/"+file+".json")
    team_match = t_d.team()
    vcaptain = team_match[1]
    captain = team_match[0]
    team_list = t_d.player
    players = []
    for i in team_list:
        if i == captain:
            tag_c = "(C)"
        elif i == vcaptain:
            tag_c = "(VC)"
        else:
            tag_c = ""
        players.append(i)
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


def scrape_with_crochet(file, match_type, team1, team2, players1, players2):
    
    v = os.popen(
        'scrapy crawl howstat -a match_type="'
        + match_type
        + '" -a team1="'
        + team1
        + '" -a team2="'
        + team2 
        + '" -a players1='
        + players1
        + ' -a players2='
        + players2
        + ' -a file="'
        + file
        + '" --loglevel DEBUG',
    )
    v.close()
    
def _crawler_Stop():
    print("done")
