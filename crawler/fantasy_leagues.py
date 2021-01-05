
"""
This modules defines all the fantasy leagues that
the project supports
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


class Scorer:
    """
    Scorer class to use different formats of the game

    :py:class `t20`: A T20 dictionary which contains scoring metrics
    :py:class `odi`: A ODI dictionary which contains scoring metrics
    :py:class `test`: A TEST dictionary which contains scoring metrics

    :param scoring_dict: A dictionary containing scoring metrics.
            Each value represents a list  where index 0 represents `T20`,
            1 represents `ODI`, 2 represents `TEST`
    """

    def __init__(self, scoring_dict):

        self.t20 = {key: scoring_dict[key][0] for key in scoring_dict}
        self.odi = {key: scoring_dict[key][1] for key in scoring_dict}
        self.test = {key: scoring_dict[key][2] for key in scoring_dict}

    def get_score(self, stats, playing_format):
        """
        Function which sums the score for that platform
        depending on the format of the game

        :param playing_format: One of `ODI`,`T20`,`TEST`
        """
        type_map = {"ODI": self.odi, "T20": self.t20, "TEST": self.test}
        return sum(type_map[playing_format][key] * stats[key] for key in stats)


class Dream11:
    """Dream11 League

    Supported platforms:
            * ODI
            * T20
            * TEST
    """

    name = "Dream11"

    batting_dict = Scorer(
        {
            "runs": [1, 1, 1],
            "boundaries": [1, 1, 1],
            "sixes": [2, 2, 2],
            "50": [8, 4, 4],
            "100": [16, 8, 8],
            "duck": [-2, -3, -4],
        }
    )

    bowling_dict = Scorer(
        {
            "wicket": [25, 25, 16],
            "4-wicket-haul": [8, 4, 4],
            "5-wicket-haul": [16, 8, 8],
            "Maiden": [4, 8, 0],
        }
    )

    wk_dict = Scorer(
        {
            "Catch": [8, 8, 8],
            "Stump": [12, 12, 12],
        }
    )
