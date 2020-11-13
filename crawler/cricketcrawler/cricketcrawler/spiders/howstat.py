from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cricketcrawler.items import MatchidItem,PlayerItem
from dateutil.parser import parse as dateparse
from scrapy import Request
class HowstatSpider(CrawlSpider):
    name = 'howstat'
    allowed_domains = ['howstat.com']
    start_urls = ["http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp"]
    rules=(
        Rule(
            LinkExtractor(allow=("/cricket/Statistics/Matches/MatchScorecard","/cricket/Statistics/Matches/MatchScoreCard"),deny=("&Print=Y","/cricket/Statistics/Players/PlayerOverview")),
            callback="parse_scorecard"
        ),
        Rule(
            LinkExtractor(allow=("/cricket/Statistics/Players/PlayerOverview"),deny=("&Print=Y","/cricket/Statistics/Players/PlayerOverviewSummary")),
            callback="parse_player"
        ),
        Rule(
            LinkExtractor(allow=("cricket/Statistics/Matches/MatchList","/cricket/Statistics/Players/PlayerListCurrent.asp"),deny=("&Print=Y",)))
    )

    def parse_player(self, response):
        name=response.selector.xpath("/html/body/table/tr[2]/td[3]/table[2]/tr/td/table[1]/tr[1]/td[1]/text()").get()
        name=name.replace("\r","").replace("\t","").replace("\n","").replace("\xa0"," ")
        matches=response.selector.xpath("/html/body/table/tr[2]/td[3]/table[2]/tr/td/table[1]/tr[8]/td[2]/text()").get()
        matches=matches.replace("\r","").replace("\t","").replace("\n","").replace("\xa0"," ")
        if len(matches[matches.find("-"):])>2:
            retired=True
        else:
            retired=False
        gametype=response.selector.xpath("/html/body/table/tr[2]/td[3]/table[1]/tr[2]/td/text()").get()
        gametype=gametype.replace("\t","")
        gametype=gametype.replace("\r","")
        gametype=gametype.replace("\n","")
        gametype=gametype.replace("  ","")
        gametype=gametype[gametype.find("-")+1:]
        gametype=gametype[1:]
        url=response.request.url

        yield PlayerItem(name=url[url.find("?PlayerID=")+10:],gametype=gametype,folder=".",longname=name,retired=retired)

    def parse_scorecard(self,response):
        """
        parses the Scorecard
        """
        datexpath="//tr[2]/td[3]/table[2]/tr[1]/td/table[1]/tr[1]/td[2]/text()"
        playerlisxpath="//table/tr/td/table/tr/td/table/tr/td/a[@class='LinkOff']"
        url=response.request.url
        matchid=url[url.find("Matches"):]
        datestr=response.selector.xpath(datexpath).get()
        date=str(dateparse(datestr))[:10]
        lis=response.selector.xpath(playerlisxpath)
        if url.find("ODI")!=-1:
            folder="ODI"
        elif url.find("T20")!=-1:
            folder="T20"
        else:
            folder="TEST"
        for i in lis:
            if i.xpath("@href").get().startswith("../Players/PlayerOverview"):
                url=i.xpath("@href").get()
                startint=url.find("?PlayerID=")
                item=MatchidItem(name=url[startint+10:],folder=folder,matchid=matchid,date=date)
                yield item
