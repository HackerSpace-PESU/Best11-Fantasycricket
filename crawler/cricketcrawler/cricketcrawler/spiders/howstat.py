from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cricketcrawler.items import ZipItem
from dateutil.parser import parse as dateparse
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
            LinkExtractor(allow="cricket/Statistics/Matches/Match",deny="&Print=Y"))
    )

    def parse_scorecard(self,response):
        datexpath="//tr[2]/td[3]/table[2]/tr[1]/td/table[1]/tr[1]/td[2]/text()"
        playerlisxpath="//table/tr/td/table/tr/td/table/tr/td/a[@class='LinkOff']"
        url=response.request.url
        matchid=url[url.find("Matches"):]
        datestr=response.selector.xpath(datexpath).get()
        date=str(dateparse(datestr))[:10]
        lis=response.selector.xpath(playerlisxpath)
        print(len(lis))
        for i in lis:
            if i.xpath("@href").get().startswith("../Players/PlayerOverview"):
                yield ZipItem(name=i.xpath("text()").get(),matchid=matchid,date=date)
                #yield response.follow(i.xpath("@href").get())
