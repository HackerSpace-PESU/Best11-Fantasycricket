import scrapy
from espncricinfo.items import ScoreItem


class MatchesSpider(scrapy.Spider):

    name = "espn-matches"
    allowed_domains = ["espncricinfo.com"]

    def start_requests(self):
        return [
            scrapy.Request(
                url="https://stats.espncricinfo.com/ci/engine/player/253802.html?class=1&orderby=start&orderbyad=reverse&template=results&type=allround&view=match",
                callback=self.parse,
            )
        ]

    def parse(self, response):

        matches = response.selector.xpath(
            "//a[@href[contains(. , '/ci/engine/match')] and @title]"
        )[:5]
        pid = response.url.split(".html")[0].split("player/")[1]
        score_dict = {
            "runs": None,
            "boundaries": None,
            "sixes": None,
            "wicket": None,
            "Maiden": None,
            "Catch": None,
            "Stump": None,
        }
        keeping_stats = response.selector.xpath(
            "//table[caption[contains(.,'Match by match list')]]//tr[td]"
        )[:5]
        for i, match in enumerate(matches):
            score_dict["Catch"] = score_dict["Stump"] = 0
            if "Test" in match.xpath("text()").get():
                score_dict["Catch"] += int(
                    keeping_stats[i].xpath("td[6]/text()").get().strip()
                )
                score_dict["Catch"] += int(
                    keeping_stats[i].xpath("td[7]/text()").get().strip()
                )
            elif (
                "ODI" in match.xpath("text()").get()
                or "T20" in match.xpath("text()").get()
            ):
                score_dict["Catch"] += int(
                    keeping_stats[i].xpath("td[4]/text()").get().strip()
                )
                score_dict["Catch"] += int(
                    keeping_stats[i].xpath("td[5]/text()").get().strip()
                )
            yield scrapy.Request(
                url="https://www.espncricinfo.com" + match.xpath("@href").get(),
                callback=self.parse_match,
                cb_kwargs={
                    "pid": pid,
                    "score_dict": score_dict,
                    "match_id": match.xpath("text()").get(),
                },
            )

    def parse_match(self, response, pid, score_dict, match_id):

        batsman = response.selector.xpath(
            "//table[@class='table batsman']//tr[td[a[@href[contains(., '"
            + pid
            + "')]]]]"
        )
        if batsman:
            score_dict["runs"] = score_dict["boundaries"] = score_dict["sixes"] = 0
            for bat in batsman:
                score_dict["runs"] += int(bat.xpath("td[3]/text()").get().strip())
                score_dict["boundaries"] += int(bat.xpath("td[6]/text()").get().strip())
                score_dict["sixes"] += int(bat.xpath("td[7]/text()").get().strip())

        bowler = response.selector.xpath(
            "//table[@class='table bowler']//tr[td[a[@href[contains(., '"
            + pid
            + "')]]]]"
        )
        if bowler:
            score_dict["wicket"] = score_dict["Maiden"] = 0
            for bowl in bowler:
                score_dict["wicket"] += int(bowl.xpath("td[3]/text()").get().strip())
                score_dict["Maiden"] += int(bowl.xpath("td[5]/text()").get().strip())

        yield ScoreItem(
            runs=score_dict["runs"],
            boundaries=score_dict["boundaries"],
            sixes=score_dict["sixes"],
            wicket=score_dict["wicket"],
            Maiden=score_dict["Maiden"],
            Catch=score_dict["Catch"],
            Stump=score_dict["Stump"],
            match_id=match_id,
        )
