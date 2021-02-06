"""
Testing for main.py
"""
import os
from fastapi.testclient import TestClient
from app.main import app
from app.fantasy_cricket.matches import Matches

client = TestClient(app)
cricket = Matches()

# pylint: disable=missing-function-docstring

def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_playing_11():

	matches = cricket.get_upcoming_match()
	for teams in matches:
		response = client.get("/playing11?team1="+ teams["team1"] + "&team2=" + teams["team2"])
		assert response.status_code == 200

def test_results():
	response = client.get("/results?match_type=1&team=India&team=England&player_team1=253802&player_team1=277916&player_team1=398438&player_team1=26421&player_team1=625383&player_team1=940973&player_team1=625371&player_team1=931581&player_team1=32540&player_team1=422108&player_team1=34102&player_team2=303669&player_team2=8917&player_team2=8608&player_team2=669855&player_team2=646847&player_team2=10617&player_team2=398778&player_team2=308967&player_team2=364788&player_team2=641423&player_team2=455524")
	assert response.status_code == 200
