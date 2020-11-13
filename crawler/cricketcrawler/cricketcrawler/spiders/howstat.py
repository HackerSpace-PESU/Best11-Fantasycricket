from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cricketcrawler.items import MatchidItem, PlayerItem, BattingItem,BowlingItem
from dateutil.parser import parse as dateparse
from scrapy import Request
from cricketcrawler.fantasy_leagues import Dream11

class HowstatSpider(CrawlSpider):
    name = "howstat"
    allowed_domains = ["howstat.com"]
    start_urls = [
        "http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp"
    ]
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    "/cricket/Statistics/Matches/MatchScorecard",
                    "/cricket/Statistics/Matches/MatchScoreCard",
                ),
                deny=("&Print=Y", "/cricket/Statistics/Players/PlayerOverview"),
            ),
            callback="parse_scorecard",
        ),
        Rule(
            LinkExtractor(
                allow=("/cricket/Statistics/Players/PlayerOverview"),
                deny=("&Print=Y", "/cricket/Statistics/Players/PlayerOverviewSummary"),
            ),
            callback="parse_player",
        ),
        Rule(
            LinkExtractor(
                allow=(
                    "cricket/Statistics/Matches/MatchList",
                    "/cricket/Statistics/Players/PlayerListCurrent.asp",
                ),
                deny=("&Print=Y",),
            )
        ),
    )

    def parse_player(self, response):
        player_ids = []
        name = response.selector.xpath(
            "/html/body/table/tr[2]/td[3]/table[2]/tr/td/table[1]/tr[1]/td[1]/text()"
        ).get()
        name = (
            name.replace("\r", "")
            .replace("\t", "")
            .replace("\n", "")
            .replace("\xa0", " ")
        )
        matches = response.selector.xpath(
            "/html/body/table/tr[2]/td[3]/table[2]/tr/td/table[1]/tr[8]/td[2]/text()"
        ).get()
        matches = (
            matches.replace("\r", "")
            .replace("\t", "")
            .replace("\n", "")
            .replace("\xa0", " ")
        )
        if len(matches[matches.find("-") :]) > 2:
            retired = True
        else:
            retired = False
        gametype = response.selector.xpath(
            "/html/body/table/tr[2]/td[3]/table[1]/tr[2]/td/text()"
        ).get()
        gametype = gametype.replace("\t", "")
        gametype = gametype.replace("\r", "")
        gametype = gametype.replace("\n", "")
        gametype = gametype.replace("  ", "")
        gametype = gametype[gametype.find("-") + 1 :]
        gametype = gametype[1:]
        url = response.request.url
        if url[url.find("?PlayerID=")+10:] not in player_ids:
            player_ids.append(url[url.find("?PlayerID=")+10:])
            yield PlayerItem(
                name=url[url.find("?PlayerID=") + 10 :],
                gametype=gametype,
                folder=".",
                longname=name,
                retired=retired,
            )

    def parse_scorecard(self, response):
        """
        parses the Scorecard
        """
        player_ids = []
        datexpath = "//tr[2]/td[3]/table[2]/tr[1]/td/table[1]/tr[1]/td[2]/text()"
        playerlisxpath = "//table/tr/td/table/tr/td/table/tr/td/a[@class='LinkOff']"
        url = response.request.url
        matchid = url[url.find("Matches") :]
        datestr = response.selector.xpath(datexpath).get()
        date = str(dateparse(datestr))[:10]
        lis = response.selector.xpath(playerlisxpath)
        scorecard = response.selector.xpath("//table/tr/td/table/tr/td/table/tr/td[@valign='top' and @align='right' and not(@class)]/text()")
        if url.find("ODI") != -1:
            folder = "ODI"
        elif url.find("T20") != -1:
            folder = "T20"
        else:
            folder = "TEST"
        players=[]
        for i in lis:
            if i.xpath("@href").get().startswith("../Players/PlayerOverview"):
                url = i.xpath("@href").get()
                startint = url.find("?PlayerID=")
                players.append(url[startint+10:])
                if url[startint+10:] not in player_ids:
                    player_ids.append(url[startint + 10:])
                    item = MatchidItem(
                        name=url[startint + 10 :], folder=folder, matchid=matchid, date=date
                    )
                    yield item
        #the -2 is the Extras extracted which should not be counted
        assert (len(players)*5)== (len(scorecard)-2),f'Extracted scorecard doesnt match number of player records'
        scoring_dict = {}
        inc = 0
        for i,score in enumerate(scorecard):
            if i>=inc and i<55+inc: #scorecard of batting first
                if score.get().strip()!='':
                    if (i-inc)%5==0: #Runs
                        scoring_dict={}
                        scoring_dict["runs"] = int(score.get().strip())
                        scoring_dict["100"] =0
                        scoring_dict["50"] =0
                        scoring_dict["duck"] =0
                        if int(score.get().strip())>=100:
                            scoring_dict["100"] = 1
                        elif int(score.get().strip())>=50:
                            scoring_dict["50"] = 1
                        elif int(score.get().strip()) == 0:
                            scoring_dict["duck"] = 1
                    elif (i-inc)%5==2: #boundaries column
                        scoring_dict["boundaries"] = int(score.get().strip())
                    elif (i-inc)%5==3: #sixes column
                        scoring_dict["sixes"] = int(score.get().strip())
                    elif (i-inc)%5==4: # aStrike rate column
                        yield BattingItem(
                            name = players[int((i-4)/5)],
                            matchid = matchid,
                            score = Dream11.batting_dict.get_score(scoring_dict,folder),
                            strike_rate= float(score.get().strip()),
                            folder = folder
                            )
            elif i>55+inc:
                if (i-inc)%5==1: #overs
                    scoring_dict={}
                    overs = float(score.get().strip())
                elif (i-inc)%5==2: #Maidens

                    scoring_dict["Maiden"] = int(score.get().strip())
                elif (i-inc)%5==4:
                    scoring_dict["wicket"] = int(score.get().strip())
                    scoring_dict["5-wicket-haul"] =0
                    scoring_dict["4-wicket-haul"] =0
                    if scoring_dict["wicket"] >=5:
                        scoring_dict["5-wicket-haul"] =1
                    elif scoring_dict["wicket"] >=4:
                        scoring_dict["4-wicket-haul"] = 1
                elif (i-inc)%5==0: #Economy
                    yield BowlingItem(
                            name= players[int((i-5)/5)],
                            matchid=matchid,
                            score= Dream11.bowling_dict.get_score(scoring_dict,folder),
                            overs=overs,
                            economy = float(score.get().strip()),
                            folder =folder
                        )
                    if i+1 == len(scorecard):
                        break
                    if '.' not in scorecard[i+1].get().strip():
                        inc = i+1