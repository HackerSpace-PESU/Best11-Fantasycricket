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

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi import FastAPI, Form, Request, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from app.fantasy_cricket.fantasy_leagues import Dream11
from app.fantasy_cricket.matches import Matches
from typing import List

# pylint: disable=missing-function-docstring
# pylint: disable=global-variable-undefined

app = FastAPI()

templates = Jinja2Templates(directory="./app/fantasy_cricket/templates")
app.mount(
    "/static", StaticFiles(directory="./app/fantasy_cricket/static"), name="static"
)


cricket = Matches()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    matches = cricket.get_upcoming_match()
    return templates.TemplateResponse(
        "index.html", {"request": request, "teams": matches}
    )


@app.post("/")
def home_post(match: str = Form(...)):

    response = RedirectResponse(
        url="/playing11?team1="
        + match.split(" vs ")[0]
        + "&team2="
        + match.split(" vs ")[-1],
        status_code=status.HTTP_302_FOUND,
    )
    return response


@app.get("/playing11", response_class=HTMLResponse)
def playing_11(request: Request, team1: str = Query(...), team2: str = Query(...)):

    match_data = cricket.get_squad_match_type([team1, team2])
    return templates.TemplateResponse(
        "Playing_11.html",
        {
            "request": request,
            "squads": [match_data["team1_squad"], match_data["team2_squad"]],
            "match_type": match_data["match_type"],
            "teams": [team1, team2],
        },
    )


@app.post("/playing11")
async def playing_11_post(
    request: Request,
    team1: str = Query(...),
    team2: str = Query(...),
    match_type: str = Query(...),
):

    playing_11 = list(jsonable_encoder(await request.form()).keys())
    playing_11.remove("Confirm")
    url = (
        "/results/?match_type="
        + match_type
        + "&team1="
        + team1
        + "&team2="
        + team2
        + "&"
    )
    for player in playing_11[0:11]:
        url += "player_team1=" + player + "&"
    for player in playing_11[11:]:
        url += "player_team2=" + player + "&"
    return RedirectResponse(url=url[:-1], status_code=status.HTTP_302_FOUND)


@app.get("/results", response_class=HTMLResponse)
def result(
    request: Request,
    team1: str,
    team2: str,
    match_type: str = Query(...),
    player_team1: List[str] = Query(...),
    player_team2: List[str] = Query(...),
):
    t_d = Dream11(team1, team2)
    t_d.fetch_fantasy_team(player_team1, player_team2, match_type)
    team = t_d.get_fantasy_team()
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "team": team,
        },
    )

@app.get("/robots.txt")
def robots():
    return FileResponse("app/robots.txt")
