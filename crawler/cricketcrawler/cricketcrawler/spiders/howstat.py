from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cricketcrawler.items import ZipItem,PlayerItem
from dateutil.parser import parse as dateparse
from scrapy import Request
class HowstatSpider(CrawlSpider):
    name = 'howstat'
    allowed_domains = ['howstat.com']
    start_urls = ["http://www.howstat.com/cricket/Statistics/Matches/MatchListMenu.asp"]
    rules=(
        Rule(
            LinkExtractor(allow=("/cricket/Statistics/Matches/MatchScorecard","/cricket/Statistics/Matches/MatchScoreCard"),deny="&Print=Y"),
            callback="parse_scorecard"
        ),
        Rule(
            LinkExtractor(allow=("/cricket/Statistics/Players/PlayerOverview"),deny=("&Print=Y","/cricket/Statistics/Players/PlayerOverviewSummary")),
            callback="parse_player"
        ),
        Rule(
            LinkExtractor(allow=("cricket/Statistics/Matches/MatchList",),deny=("&Print=Y","/cricket/Statistics/Players/PlayerOverviewSummary")))
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
        gametype=gametype.replace("  ","")
        gametype=gametype[gametype.find("-")+1:]
        print(response.meta,response.request.meta,response.url)
        #yield PlayerItem(name=response.meta["name"],long_name=name,gametype=gametype,retired=retired)

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
        #print(len(lis))
        for i in lis:
            if i.xpath("@href").get().startswith("../Players/PlayerOverview"):
                yield ZipItem(name=i.xpath("text()").get(),matchid=matchid,date=date)
                #request=Request(response.urljoin(i.xpath("@href").get()))
                #request.meta["playername"]=i.xpath("text()").get()
                #yield request

#http://howstat.com/Players/PlayerOverview_T20.asp?PlayerID=5197