"""
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
from scrapy import Request, Spider
from crawler.fantasy_leagues import Dream11
from crawler.items import PlayerItem


class HowstatSpider(Spider):
    """
    Spider which crawls through howstat.com
    """
    name = "howstat"
    allowed_domains = ["howstat.com"]

    start_urls = ["http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp"]
    def __init__(self, players1="", players2="", match_type="", *args, **kwargs):
        super(HowstatSpider, self).__init__(*args, **kwargs)
        self.names = {
            "last": {self.team1: [], self.team2: []},
            "first": {self.team1: [], self.team2: []},
        }
        for player in players1.split(","):
            player_id = player.split()
            if (
                    player_id[0].lower().strip() == "de"
                    or player_id[0].lower().strip() == "du"
                    or player_id[0].lower().strip() == "van"
            ):
                player_id = [' '.join(player_id)]
            if len(player_id) == 1:
                self.names["last"][self.team1].append(player_id[0].lower().strip())
                self.names["first"][self.team1].append("")
            elif len(player_id) >= 1:
                self.names["last"][self.team1].append(player_id[-1].lower().strip())
                self.names["first"][self.team1].append(player_id[0].lower().strip())
        for player in players2.split(","):
            player_id = player.split()
            if len(player_id) == 1:
                self.names["last"][self.team2].append(player_id[0].lower().strip())
                self.names["first"][self.team2].append("")
            elif len(player_id) >= 1:
                self.names["last"][self.team2].append(player_id[-1].lower().strip())
                self.names["first"][self.team2].append(player_id[0].lower().strip())
        assert (
            len(self.names["last"][self.team1])
            == 11
            == len(self.names["first"][self.team1])
            == len(self.names["first"][self.team2])
            == len(self.names["last"][self.team2])
        )
        if match_type == "TEST":
            self.match_type = ""
        else:
            self.match_type = "_" + match_type
        self.matches = {}
        self.count = 0

    def parse(self, response):
        """
        Returns a request for the player found in the parsed url
        """
        comma_map = {
            "India": 1,
            "Australia": 1,
            "New Zealand": 1,
            "England": 1,
            "Bangladesh": 0,
            "South Africa": 1,
            "West Indies": 1,
            "Pakistan": 0,
            "Afghanistan": 0,
            "Sri Lanka": 1,
        }
        teams = {
            self.team1: response.selector.xpath(
                "//table[@class='TableLined']/tr[td[3]/text()[contains(.,'"
                + self.team1
                + "')]]/td[1]"
            ),
            self.team2: response.selector.xpath(
                "//table[@class='TableLined']/tr[td[3]/text()[contains(.,'"
                + self.team2
                + "')]]/td[1]"
            ),
        }
        players = {}
        for team in teams:
            players[team] = []
            for player in teams[team]:
                player_id = player.xpath("a/text()").get()
                if comma_map[team]:
                    player_id = player_id.split(",")
                    try:
                        i = self.names["last"][team].index(player_id[0].lower().strip())
                        if self.names["first"][team][i] == "":
                            players[team].append(player.xpath("a"))
                        else:
                            for initial in player_id[1].split():
                                if (
                                        self.names["first"][team][i][0].lower()
                                        == initial.lower().strip()
                                ):
                                    players[team].append(player.xpath("a"))
                                    break
                    except ValueError:
                        pass
                else:
                    player_id = (player_id.split()[0], player_id.split()[-1])
                    try:
                        i = self.names["last"][team].index(player_id[1].lower().strip())
                        if self.names["first"][team][i] == "":
                            players[team].append(player.xpath("a"))
                        else:
                            if player_id[0].lower().strip() in self.names["first"][team]:
                                players[team].append(player.xpath("a"))
                    except ValueError:
                        pass
        for team in players:
            for player in players[team]:
                player_id = player.xpath("@href").get().split("?")[1]
                yield Request(
                    "http://www.howstat.com/cricket/Statistics/Players/PlayerProgressSummary"
                    + self.match_type
                    + ".asp?"
                    + player_id,
                    callback=self.parse_last5,
                    cb_kwargs={"team": team},
                )

    def parse_last5(self, response, team):
        """
        Gets the data of last 5 games for each player
        """
        name = (
            response.xpath("//td[contains(@class, 'Banner')]/text()")
            .get()
            .strip()
            .split("(")[0]
            .strip()
        )
        if self.match_type != "":
            matches = response.xpath(
                '//table[@class = "TableLined"]/tr[position()>last()-5]/td[2]/a'
            )
        else:
            matches = response.xpath(
                '//table[@class = "TableLined"]/tr[position()>last()-10]/td[2]/a'
            )
        crawl = False
        if len(matches) >= 5:
            crawl = True
            matches = matches[len(matches)-5:]
        for match in matches:
            if crawl:
                yield Request(
                    "http://www.howstat.com/cricket/Statistics"
                    + match.xpath("@href").get().split("..")[1],
                    callback=self.parse_scorecard,
                    cb_kwargs={
                        "name": name,
                        "pid" : response.url.split("?")[-1],
                        "team" : team,
                        "date" : match.get().split('>')[1].split('<')[0]
                    },
                    dont_filter=True,
                )

    def parse_scorecard(self, response, name, pid, team, date):
        """
        parses the Scorecard
        """
        scorelisxpath = (
            "//table/tr/td/table/tr/td/table/tr[td[a[@href[contains(.,'"
            + pid
            + "')]]]]"
        )
        lis = response.selector.xpath(scorelisxpath)
        batting_dict = {}
        bowling_dict = {}
        keeping_dict = {}
        role = None
        for score in lis:
            if score.xpath("td[1]/text()[contains(.,'†')]").get():
                role = "wk"
            elif score.xpath("td[2]/text()[contains(.,'.')]"):
                if "Maiden" not in bowling_dict:
                    bowling_dict["Maiden"] = 0
                bowling_dict["Maiden"] += int(score.xpath("td[3]/text()").get().strip())
                if "wicket" not in bowling_dict:
                    bowling_dict["wicket"] = 0
                bowling_dict["wicket"] += int(score.xpath("td[5]/text()").get().strip())
                if "4-wicket-haul" not in bowling_dict:
                    bowling_dict["4-wicket-haul"] = 0
                if "5-wicket-haul" not in bowling_dict:
                    bowling_dict["5-wicket-haul"] = 0
                if int(score.xpath("td[5]/text()").get().strip()) >= 5:
                    bowling_dict["5-wicket-haul"] += 1
                elif int(score.xpath("td[5]/text()").get().strip()) >= 4:
                    bowling_dict["4-wicket-haul"] += 1
            else:
                current = score
                for _ in range(0, 4):
                    if role == "wk":
                        break
                    current = current.xpath("following-sibling::tr")
                    if current.xpath("td[1][contains(.,'Extras')]"):
                        role = "bowl"
                        break
                if "runs" not in batting_dict:
                    batting_dict["runs"] = 0
                if score.xpath("td[3]/text()").get().strip() == "":
                    batting_dict["runs"] = 0
                    batting_dict["boundaries"] = 0
                    batting_dict["sixes"] = 0
                    batting_dict["50"] = 0
                    batting_dict["100"] = 0
                    batting_dict["duck"] = 0
                    continue
                batting_dict["runs"] += int(score.xpath("td[3]/text()").get().strip())
                if "boundaries" not in batting_dict:
                    batting_dict["boundaries"] = 0
                batting_dict["boundaries"] += int(
                    score.xpath("td[5]/text()").get().strip()
                )
                if "sixes" not in batting_dict:
                    batting_dict["sixes"] = 0
                batting_dict["sixes"] += int(score.xpath("td[6]/text()").get().strip())
                if "50" not in batting_dict:
                    batting_dict["50"] = 0
                if "100" not in batting_dict:
                    batting_dict["100"] = 0
                if "duck" not in batting_dict:
                    batting_dict["duck"] = 0
                if int(score.xpath("td[3]/text()").get().strip()) >= 100:
                    batting_dict["100"] += 1
                elif int(score.xpath("td[3]/text()").get().strip()) >= 50:
                    batting_dict["50"] += 1
                elif (
                        int(score.xpath("td[3]/text()").get().strip()) == 50
                        and role != "bowl"
                    ):
                    batting_dict["duck"] += 1
        if role == "wk":
            wk_score = score.xpath(
                "//table/tr/td/table/tr/td/table/tr[td[2][@valign and @width]/text()[contains(.,'"
                + name.split()[-1].strip()
                + "')]]"
            ).xpath("td[2]/text()")
            if wk_score:
                if "Catch" not in keeping_dict:
                    keeping_dict["Catch"] = 0
                if "Stump" not in keeping_dict:
                    keeping_dict["Stump"] = 0
                for wk_s in wk_score:
                    if "c †" in wk_s.get():
                        keeping_dict["Catch"] += 1
                    elif "st †" in wk_s.get():
                        keeping_dict["Stump"] += 1

        if bowling_dict != {} and role != "bowl":
            role = "all"
        elif bowling_dict == {} and role != "wk":
            role = "bat"
        score = 0
        match_type = {"_ODI": "ODI", "_T20": "T20", "": "TEST"}
        if role == "wk":
            score += Dream11.wk_dict.get_score(
                keeping_dict, match_type[self.match_type]
            )
            score += Dream11.batting_dict.get_score(
                batting_dict, match_type[self.match_type]
            )
        elif role == "bowl":
            score += Dream11.bowling_dict.get_score(
                bowling_dict, match_type[self.match_type]
            )
        elif role == "all":
            score += Dream11.bowling_dict.get_score(
                bowling_dict, match_type[self.match_type]
            )
            score += Dream11.batting_dict.get_score(
                batting_dict, match_type[self.match_type]
            )
        elif role == "bat":
            score += Dream11.batting_dict.get_score(
                batting_dict, match_type[self.match_type]
            )

        yield PlayerItem(
            name=name, score=score, role=role, date=date, team=team, file=self.file
        )
