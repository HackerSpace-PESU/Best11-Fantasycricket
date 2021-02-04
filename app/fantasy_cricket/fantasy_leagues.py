from app.fantasy_cricket.team import Team


class Dream11(Team):
    """Dream11 League

    Supported formats:
        * ODI
        * T20
        * TEST
    """

    name = "Dream11"

    batting_dict = {
        "runs": [1, 1, 1],
        "boundaries": [1, 1, 1],
        "sixes": [2, 2, 2],
        "50": [4, 4, 8],
        "100": [8, 8, 16],
        "duck": [-4, -3, -2],
    }

    bowling_dict = {
        "wicket": [16, 25, 25],
        "4-wicket-haul": [4, 4, 8],
        "5-wicket-haul": [8, 8, 16],
        "Maiden": [0, 8, 4],
    }

    wk_dict = {
        "Catch": [8, 8, 8],
        "Stump": [12, 12, 12],
    }
