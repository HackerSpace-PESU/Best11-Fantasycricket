"""
Testing for main.py
"""
import os
from fastapi.testclient import TestClient
from app.main import app
from app.fantasy_cricket.utils import Matches

client = TestClient(app)
cricket = Matches()

# pylint: disable=missing-function-docstring

def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_home_post():
	teams = [
        [match[0]["name"], match[1]["name"]]
        for match in cricket.get_match()
    ]
	for team in teams:
		response = client.post("/", data={"match": team[0]+" vs "+team[1]})
		assert response.status_code == 302
	
def test_playing_11():
	teams = [
        [match[0]["name"], match[1]["name"]]
        for match in cricket.get_match()
    ]
	for team in teams:
		response = client.get("/playing11?team1="+team[0]+"&team2="+team[1], 
								data={"match": team[0]+" vs "+team[1]})
		assert response.status_code == 200
