import scrapy
from espncricinfo.items import PlayerItem


class PlayerListSpider(scrapy.Spider):

    name = "espn-players"
    allowed_domains = ["espncricinfo.com"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.espncricinfo.com/ci/content/player/253802.html",
                callback=self.parse,
            )
        ]

    def parse(self, response):

        name = response.selector.xpath("//div[@class='ciPlayernametxt']/div/h1/text()")
        role = response.selector.xpath(
            "//p[@class='ciPlayerinformationtxt' and b/text()[contains(.,'Playing role')]]/span/text()"
        )
        image = response.selector.xpath(
            "//img[@src[contains(.,'espncricinfo.com/inline/content')]]"
        ).xpath("@src")

        yield PlayerItem(
            name=name.get(),
            role=role.get(),
            image=image.get(),
        )
