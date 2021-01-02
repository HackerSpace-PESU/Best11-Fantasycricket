from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cricketcrawler.items import PlayerItem
from dateutil.parser import parse as dateparse
import datetime
from urllib.parse import urljoin
from scrapy import Request
import scrapy
from cricketcrawler.fantasy_leagues import Dream11


class HowstatSpider(scrapy.Spider):
    name = "howstat"
    allowed_domains = ["howstat.com"]

    start_urls = [
        "http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp"
    ]

    def __init__(self, players1="", players2="", match_type="", *args, **kwargs):
        super(HowstatSpider, self).__init__(*args, **kwargs)
        self.names = {
            "last": {self.team1: [], self.team2: []},
            "first": {self.team1: [], self.team2: []},
        }
        for player in players1.split(","):
            p = player.split()
            if len(p) == 1:
                self.names["last"][self.team1].append(p[0].lower().strip())
                self.names["first"][self.team1].append("")
            elif len(p) >= 1:
                self.names["last"][self.team1].append(p[-1].lower().strip())
                self.names["first"][self.team1].append(p[0].lower().strip())
        for player in players2.split(","):
            p = player.split()
            if len(p) == 1:
                self.names["last"][self.team2].append(p[0].lower().strip())
                self.names["first"][self.team2].append("")
            elif len(p) >= 1:
                self.names["last"][self.team2].append(p[-1].lower().strip())
                self.names["first"][self.team2].append(p[0].lower().strip())
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
        self.count=0
    def parse(self, response):
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
                p = player.xpath("a/text()").get()
                if comma_map[team]:
                    p = p.split(",")
                    try:
                        i = self.names["last"][team].index(p[0].lower().strip())
                        if self.names["first"][team][i] == "":
                            players[team].append(player.xpath("a"))
                        else:
                            for initial in p[1].split():
                                if (
                                    self.names["first"][team][i][0].lower()
                                    == initial.lower().strip()
                                ):
                                    players[team].append(player.xpath("a"))
                                    break
                    except ValueError:
                        pass
                else:
                    p = (p.split()[0], p.split()[-1])
                    try:
                        i = self.names["last"][team].index(p[1].lower().strip())
                        if self.names["first"][team][i] == "":
                            players[team].append(player.xpath("a"))
                        else:
                            if p[0].lower().strip() in self.names["first"][team]:
                                players[team].append(player.xpath("a"))
                    except ValueError:
                        pass
        for team in players:
            for player in players[team]:
                player_id = player.xpath("@href").get().split("?")[1]
                yield scrapy.Request(
                    "http://www.howstat.com/cricket/Statistics/Players/PlayerProgressSummary"
                    + self.match_type
                    + ".asp?"
                    + player_id,
                    callback=self.parse_last5,
                    cb_kwargs={"team": team},
                )

    def parse_last5(self, response, team):
        if self.match_type != "" and self.match_type in response.url:
            name = (
                response.xpath("//td[contains(@class, 'Banner')]/text()")
                .get()
                .strip()
                .split("(")[0]
                .strip()
            )

            matches = response.xpath(
                '//table[@class = "TableLined"]/tr[position()>last()-5]/td[2]/a'
            )
            if len(matches) < 5:
                return
            for match in matches:
                yield scrapy.Request(
                    "http://www.howstat.com/cricket/Statistics"
                    + match.xpath("@href").get().split("..")[1],
                    callback=self.parse_scorecard,
                    cb_kwargs={
                        "name": name,
                        "pid": response.url.split("?")[-1],
                        "team": team,
                    },
                    dont_filter=True
                )

    def parse_scorecard(self, response, name, pid, team):
        """
        parses the Scorecard
        """
        print(response.url,name)
        player_ids = []
        datexpath = "//tr[2]/td[3]/table[2]/tr[1]/td/table[1]/tr[1]/td[2]/text()"
        scorelisxpath = (
            "//table/tr/td/table/tr/td/table/tr[td[a[@href[contains(.,'"
            + pid
            + "')]]]]"
        )
        url = response.request.url
        datestr = response.selector.xpath(datexpath).get()
        date = str(dateparse(datestr))[:10]
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
                for i in range(0, 4):
                    if role == "wk":
                        break
                    current = current.xpath("following-sibling::tr")
                    if current.xpath("td[1][contains(.,'Extras')]"):
                        role = "bowl"
                        break
                if "runs" not in batting_dict:
                    batting_dict["runs"] =0
                if score.xpath("td[3]/text()").get().strip() == "":
                    batting_dict["runs"] = 0
                    batting_dict["boundaries"] = 0
                    batting_dict["sixes"] = 0
                    batting_dict["50"] = 0
                    batting_dict["100"] = 0
                    batting_dict["duck"] = 0
                    continue
                batting_dict["runs"]+=int(score.xpath("td[3]/text()").get().strip())        
                if "boundaries" not in batting_dict:
                    batting_dict["boundaries"] = 0
                batting_dict["boundaries"]+=int(score.xpath("td[5]/text()").get().strip())
                if "sixes" not in batting_dict:
                    batting_dict["sixes"] = 0    
                batting_dict["sixes"]+=int(score.xpath("td[6]/text()").get().strip())
                if "50" not in batting_dict:
                    batting_dict["50"] = 0
                if "100" not in batting_dict:
                    batting_dict["100"] = 0
                if "duck" not in batting_dict:
                    batting_dict["duck"] = 0
                if int(score.xpath("td[3]/text()").get().strip())>=100:
                    batting_dict["100"]+=1
                elif int(score.xpath("td[3]/text()").get().strip())>=50:
                    batting_dict["50"]+=1
                elif int(score.xpath("td[3]/text()").get().strip())==50 and role!="bowl":
                    batting_dict["duck"]+=1
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

        if bowling_dict!={} and role!="bowl":
            role = "all"
        elif bowling_dict == {} and role !="wk":
            role="bat"
        score = 0
        match_type = {
            "_ODI":"ODI",
            "_T20":"T20",
            "":"TEST"
        }
        if role=="wk":
            score += Dream11.wk_dict.get_score(keeping_dict,match_type[self.match_type])
            score += Dream11.batting_dict.get_score(batting_dict,match_type[self.match_type])
        elif role=="bowl":
            score+=Dream11.bowling_dict.get_score(bowling_dict,match_type[self.match_type])
        elif role=="all":
            score+= Dream11.bowling_dict.get_score(bowling_dict,match_type[self.match_type])
            score += Dream11.batting_dict.get_score(batting_dict,match_type[self.match_type])
        elif role=="bat":
            score += Dream11.batting_dict.get_score(batting_dict,match_type[self.match_type])

        yield PlayerItem(
            name = name,
            score=score,
            role= role,
            date = date,
            team = team,
            file = self.file
        )

