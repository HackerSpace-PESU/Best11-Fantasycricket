import scrapy
import datetime
import json
from espncricinfo.items import LiveMatchItem


class LiveSpider(scrapy.Spider):

    name = "espn-live"
    allowed_domains = ["espncricinfo.com"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://www.espncricinfo.com/live-cricket-match-schedule-fixtures",
                callback=self.parse,
            )
        ]

    def parse(self, response):

        matches = response.selector.xpath("//a[@class = 'match-info-link-FIXTURES']")
        now = datetime.datetime.now().date()

        for match in matches:

            try:
                if (
                    datetime.datetime.strptime(
                        match.xpath("div/div/div/span/text()").get().split(",")[0],
                        "%d-%b-%Y",
                    ).date()
                    - now
                ).days <= 7:
                    match_link = [
                        match.xpath("@href").get()
                        for team_div in match.xpath(
                            "div/div/div[@class='teams']/div[@class='team']"
                        )
                        if team_div.xpath("div/p/text()").get()
                        in [
                            "India",
                            "Australia",
                            "England",
                            "Bangladesh",
                            "New Zealand",
                            "South Africa",
                            "Pakistan",
                            "Sri Lanka",
                            "West Indies",
                            "Afghanistan",
                        ]
                    ]
                    if match_link:
                        yield scrapy.Request(
                            url="https://www.espncricinfo.com/matches/engine/match/"
                            + match_link[0]
                            .split("/live-cricket-score")[0]
                            .split("-")[-1]
                            + ".json",
                            callback=self.parse_match,
                        )
            except ValueError:
                pass

    def parse_match(self, response):

        match_data = json.loads(response.text)
        team1_squad = []
        team2_squad = []
        for squad in match_data["team"][0]["squad"]:
            team1_squad.append(
                {"name": squad["card_long"], "player_id": squad["object_id"]}
            )
        for squad in match_data["team"][1]["squad"]:
            team2_squad.append({"name": squad["card_long"], "id": squad["object_id"]})

        yield LiveMatchItem(
            team1=match_data["match"]["team1_name"],
            team2=match_data["match"]["team2_name"],
            match_id=match_data["match"]["international_class_id"],
            team1_squad=team1_squad,
            team2_squad=team2_squad,
            team1_id=match_data["match"]["team1_id"],
            team2_id=match_data["match"]["team2_id"],
        )
