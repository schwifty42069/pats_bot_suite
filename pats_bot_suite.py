import json
import time
from threading import Thread
import threading
import requests
from bs4 import BeautifulSoup as Soup
from praw import *
import praw.exceptions
import configparser

config = configparser.RawConfigParser()
config.read("config/config.properties")
username = config.get('user', 'username')
password = config.get('user', 'password')
client_id = config.get('api', 'client_id')
client_secret = config.get('api', 'client_secret')
user_agent = config.get('api', 'user_agent')


# This is the main control class that runs a thread for streaming comment/submission objects
class PatsBotSuite(Thread):
    def __init__(self, mode):
        super().__init__()
        self.sub = "Patriots"
        self.mode = mode
        self.reddit = Reddit(
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.article_kws = ['https://nesn', 'https://www.patspulpit', 'https://weei', 'https://patriotswire']
        self._stop_event = threading.Event()
        self.nesn_reply_footer = "\n***\n^I ^am ^the ^FuckNESNBot, ^part ^of ^the ^r/patriots ^utility ^bot! ^Click " \
                                 "^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                                 "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.weei_reply_footer = "\n***\n^I ^am ^the ^WEEIBot, ^part ^of ^the ^r/patriots ^utility ^bot! ^Click " \
                                 "^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                                 "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.slater_footer = "\n***\n^I ^am ^the ^slater ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! ^Click " \
                             "^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                             "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.ftj_footer = "\n***\n^I ^am ^the ^FTJs ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! ^Click " \
                          "^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                          "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.refs_footer = "\n***\n^I ^am ^the ^fuck ^the ^refs ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! " \
                           "^Click ^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                           "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.pp_footer = "\n***\n^I ^am ^the ^patspulpit ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! " \
                         "^Click ^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                         "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.boohoo = "\n***\n^I ^am ^the ^boohoo ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! " \
                      "^Click ^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                      "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        self.pw_footer = "\n***\n^I ^am ^the ^patriotswire ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! " \
                         "^Click ^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                         "^my ^creator! ^| ^[Github](https://github.com/schwifty42069/pats_bot_suite)"

        print("\nAuthenticated as {}!\n".format(self.reddit.user.me()))

    """The PatsBotSuite class has a mode attribute that determines if the thread is streaming comments or submissions. 
       If it's in submissions mode, it iterates over the contents of the article_kws attribute, if a match is found 
       between a keyword and the url attribute of the submission object, a scraper object is created and passed the url 
       attribute of the submission object."""

    def stream_subreddit(self):
        if self.mode == "submissions":
            print("\nStreaming submissions...\n")
            for submission in self.reddit.subreddit(self.sub).stream.submissions(skip_existing=True):
                for kw in self.article_kws:
                    if kw in submission.url:
                        scraper = ArticleScraper(submission.url)
                        scraper.scrape_article()
                        self.build_successful_reply(scraper.content, submission)
                if "post-game thread" in submission.title.lower():
                    pgs = PostGameStatScraper("patriots")
                    submission.reply(pgs.build_pg_reply())

        # felt like this was simple enough to just run in an if/else block
        elif self.mode == "comments":
            print("\nStreaming comments...\n")
            for comment in self.reddit.subreddit(self.sub).stream.comments(skip_existing=True):
                try:
                    if "!slater" in comment.body.lower():
                        print("\nSaying Awwww yeahhhh!\n")
                        comment.reply("## Awwwwwwwww yeahhhhhhhhhhhh!\n{}\n".format(self.slater_footer))
                    elif "!jets" in comment.body.lower() and str(comment.author) != "PatsUtilityBot":
                        print("\nSaying fuck the jets!\n")
                        comment.reply("## Fuck the Jets!\n{}\n".format(self.ftj_footer))
                    elif "!refs" in comment.body.lower():
                        print("\nSaying fuck the refs!\n")
                        comment.reply("## Fuck the refs!\n{}\n".format(self.refs_footer))
                    elif "!boohoo" in comment.body.lower():
                        print("\nSaying boohoo!\n")
                        comment.reply("## Boohoo! My team wost to da Patwiots! D:\n{}\n".format(self.boohoo))
                except praw.exceptions.APIException:
                    print("\nHitting rate limiter...\n")
                    time.sleep(10)
                    continue

    """The content arg that is passed to this method is a dict containing the name of the site,
       (used to choose the correct reply footer) the title of the article, the author/time of the article, 
       and the formatted article itself (formatting is done with some hacky methods in the ArticleScraper class)
       The submission object is then used to send the formatted reply."""

    def build_successful_reply(self, content, submission):
        if content['site'] == "nesn":
            footer = self.nesn_reply_footer
        elif content['site'] == "weei":
            footer = self.weei_reply_footer
        elif content['site'] == "patspulpit":
            footer = self.pp_footer
        elif content['site'] == "patriotswire":
            footer = self.pw_footer
        else:
            footer = ""
        reply = "## {}\n\n" \
                "by {}" \
                "\n***\n" \
                "\n{}\n" \
                "\n{}\n".format(content['title'], content['author'], content['article'], footer)
        print("\nReplying with {}\n".format(reply))
        sent = False
        while not sent:
            try:
                submission.reply(reply)
                sent = True
            except praw.exceptions.APIException:
                print("\nHitting rate limiter..\n")
                time.sleep(60)
                continue

    # for when I inevitably break something and need to print the reply without a submission object
    def dry_reply(self, content):
        footer = ""
        if content['site'] == "nesn":
            footer = self.nesn_reply_footer
        elif content['site'] == "weei":
            footer = self.weei_reply_footer
        elif content['site'] == "patriotswire":
            footer = self.pw_footer
        elif content['site'] == "patspulpit":
            footer = self.pp_footer

        reply = "## {}\n\n" \
                "by {}" \
                "\n***\n" \
                "\n{}\n" \
                "\n{}\n".format(content['title'], content['author'], content['article'], footer)
        print("\n{}\n".format(reply))

    def run(self):
        while True:
            try:
                self.stream_subreddit()
            except KeyboardInterrupt:
                self.stop()
                return

    def stop(self):
        print("\nStopping..\n")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ArticleScraper(object):
    def __init__(self, link):
        super().__init__()
        self.link = link
        if "https://nesn" in self.link:
            self.site = "nesn"
        elif "https://weei" in self.link:
            self.site = "weei"
        elif "https://www.patspulpit" in link:
            self.site = "patspulpit"
        elif "https://patriotswire" in link:
            self.site = "patriotswire"
        else:
            self.site = ""
        self.bsoup = Soup(requests.get(self.link).text, 'html.parser')
        self.content = {}

    # a hacky little static method for identifying and formatting numbered lists, article passed as arg and returned
    @staticmethod
    def check_for_numbered_list(article):
        words = article.split()
        word_count = len(words)
        if "1." in words and "2." in words and "3." in words:
            for x in range(1, 101):
                if "{}.".format(str(x)) in words:
                    words.insert(words.index("{}.".format(str(x))), "\n\n")
        if word_count != len(words):
            article = ""
            for word in words:
                article += "{} ".format(word)
        return article

    """Another hacky little static method mainly for articles that lack new-line formatting ("\n")
       reddit ignores extra spaces, so articles with existing new-line formatting still look nice.
       The article is passed as an arg and returned by the method."""

    @staticmethod
    def double_new_lines(article):
        lines = article.split("\n")
        article = ""
        for line in lines:
            if "pic.twitter.com" in line:
                formatted_line = line.split("pic.twitter.com/")[0]
                formatted_line_words = formatted_line.split()
                formatted_line_words.insert(len(formatted_line_words), "[picture/video]({})".format(
                    "https://pic.twitter.com/{}".format(line.split("pic.twitter.com/")[1])))
                line = ""
                for word in formatted_line_words:
                    line += "{} ".format(word)
            if line.isupper():
                article += "**{}**\n\n".format(line)
            else:
                article += "{}\n\n".format(line)
        return article

    """The methods below are the meat and potatoes of the ArticleScraper class. The class is instantiated with the link 
       of the article as an arg, which determines the site attribute. The site attribute is then used to determine
       which method is called from the scrape_article method. The methods don't return anything,
       they instead update the content attribute of the class, which is the dict mentioned 
       earlier containing all of the data required to build a formatted reply."""

    def scrape_nesn(self):
        print("\nScraping article...\n")
        title = self.bsoup.find("title").text.split(" |")[0]
        author = self.bsoup.find("header", {"class": "entry-header"}).text.split("by ")[1].split("\t")[0]
        if "”\n[nesn_embed_the_score team=”patriots”[\n" in self.bsoup.find("p").text:
            article = self.bsoup.find("p").text.split("”\n[nesn_embed_the_score team=”patriots”[\n")[0] + \
                      self.bsoup.find("p").text.split("”\n[nesn_embed_the_score team=”patriots”[\n")[1].split(
                          "Thumbnail")[0]
        else:
            article = self.bsoup.find("p").text.split("Thumbnail")[0]
        formatted_article = self.check_for_numbered_list(self.double_new_lines(article))
        self.content.update({"site": self.site, "title": title, "author": author, "article": formatted_article})

    def scrape_weei(self):
        print("\nScraping article...\n")
        article = ""
        title = self.bsoup.find("h1", {"class": "header__primary"}).text
        author = self.bsoup.find("a", {"class": "author__name"}).text
        try:
            article_time = self.bsoup.find("div", {"class": "item__date--created heading field field-name-extra-date-"
                                                            "created field-type-extra-date-created field-label-hidden"}) \
                .text.split("\r\n                        ")[1].split("                    ")[0]
        except IndexError:
            article_time = self.bsoup.find("div", {"class": "item__date--created heading field field-name-extra-date-"
                                           "created field-type-extra-date-created field-label-hidden"}) \
                .text.split("                    ")[1].strip("     ")
        author = "{} on {}".format(author, article_time)
        for p in self.bsoup.findAll("p"):
            if "93.7" not in p.text and "Related:" not in p.text and "RADIO.COM Sports" not in p.text:
                article += "{} \n".format(p.text)
        formatted_article = self.check_for_numbered_list(self.double_new_lines(article))
        self.content.update({"site": self.site, "title": title, "author": author, "article":
                            formatted_article.split("© 2019 Entercom Communications Corp. All rights reserved.")[0]})
        return

    def scrape_pats_pulpit(self):
        print("\nScraping article...\n")
        article = ""
        title = self.bsoup.find("h1").text
        article_time = self.bsoup.find("time", {"class": "c-byline__item"}).text.split("\n          ")[1] \
            .split("\n        ")[0]
        author = "{} on {}".format(self.bsoup.find("span", {"class": "c-byline__author-name"}).text, article_time)
        for x in range(2, len(self.bsoup.findAll("p"))):
            article += "{}\n".format(self.bsoup.findAll("p")[x].text)
        formatted_article = self.check_for_numbered_list(self.double_new_lines(article))
        self.content.update({"site": self.site, "title": title, "author": author, "article": formatted_article})
        return

    def scrape_pats_wire(self):
        print("\nScraping article...\n")
        title = self.bsoup.find("title").text
        author = "{} {}".format(self.bsoup.find("a", {"class": "author url fn"}).text,
                                self.bsoup.find("span", {"class": "article__author__date"}).text)
        article = self.bsoup.find("div", {"class": "articleBody"}).text.split("Gallery")[0]
        formatted_article = self.check_for_numbered_list(self.double_new_lines(article))
        self.content.update({"site": self.site, "title": title, "author": author, "article": formatted_article})
        return

    def scrape_article(self):
        if self.site == "nesn":
            self.scrape_nesn()

        elif self.site == "weei":
            self.scrape_weei()

        elif self.site == "patspulpit":
            self.scrape_pats_pulpit()

        elif self.site == "patriotswire":
            self.scrape_pats_wire()
        return


"""The PostGameStatScraper class is used to fetch post-game stats from nfl.com. While the thread from the PatsBotSuite 
   class is in submissions mode, it searches the title of submissions for the keywords "post-game thread", if found, a 
   PostGameStatScraper object is created and a formatted reply comprised of markdown tables is built and sent."""


class PostGameStatScraper(object):
    def __init__(self, team):
        self.sp_header = "\n| Team | Quarter | Type | Description |\n|:--:|:--:|:--:|:--|"
        self.sbq_header = "\n| Team | Q1 | Q2 | Q3 | Q4 | Total |\n|:--:|:--:|:--:|:--:|:--:|:--:|"
        self.box_header = "\n| Team | Penalties | Rushing Yards | Net Passing Yards | Scrim. Yards |" \
                          " Time of Possession | Turnovers |\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
        self.score_by_quarter = []
        self.scoring_plays = []
        self.box = []
        self.pgs = "\n***\n^I ^am ^the ^post-game ^stats ^bot, ^part ^of ^the ^r/patriots ^utility ^bot! ^Click " \
                   "^[here](https://www.reddit.com/message/compose/?to=apt-get-schwifty) ^to ^message " \
                   "^my ^creator!"

        self.team = team
        self.root_url = "https://www.nfl.com/scores"
        self.game_json = self.get_game_json()

    # These methods basically parse raw json out of the html of the page, kind of hacky
    def get_recap_link(self):
        json_data = {}
        req = requests.get(self.root_url)
        bsoup = Soup(req.text, 'html.parser')
        for s in bsoup.findAll("script"):
            if "__INITIAL_DATA__" in s.text:
                json_data = json.loads(s.text.split("__INITIAL_DATA__ = ")[1].split(";\n")[0])
        # Could modify this to fetch this data for any given team
        for game in json_data['uiState']['scoreStripGames']:
            if not game['status']['isUpcoming'] and self.team.lower() in game['status']['gameLink']:
                return "https://www.nfl.com" + game['status']['gameLink']

    def get_game_json(self):
        try:
            req = requests.get(self.get_recap_link())
            bsoup = Soup(req.text, 'html.parser')
            for s in bsoup.findAll("script"):
                if "__INITIAL_DATA__" in s.text:
                    return json.loads(s.text.split("__INITIAL_DATA__ = ")[1].split(";\n")[0])
        except requests.exceptions.MissingSchema:
            print("\nNo game data was found!\n")
            return

    def fetch_scoring_plays(self):
        score_type = ''
        for p in self.game_json['instance']['gameDetails']['plays']:
            if p['scoringPlay'] and p['playType'] != "XP_KICK":
                if "TOUCHDOWN" in p['shortDescription']:
                    score_type = "TD"
                elif "field goal" in p['shortDescription']:
                    score_type = "FG"
                elif "SAFETY" in p['shortDescription']:
                    score_type = "SAFETY"
                elif "TWO-POINT" in p['shortDescription']:
                    score_type = "2PT"
                self.format_scoring_plays(p['scoringTeam']['nickName'], p['quarter'], score_type, p['shortDescription'])
        return

    def fetch_score_by_quarter(self):
        v_final_pts = []
        h_final_pts = []
        team_list = []
        pts_total = []
        team_key_list = ['visitorTeam', 'homeTeam']
        vp = ['visitorPointsQ1', 'visitorPointsQ2', 'visitorPointsQ3', 'visitorPointsQ4']
        hp = ['homePointsQ1', 'homePointsQ2', 'homePointsQ3', 'homePointsQ4']
        totals_key_list = ['visitorPointsTotal', 'homePointsTotal']
        for t in team_key_list:
            team_list.append(self.game_json['instance']['gameDetails'][t]['nickName'])
        for q in vp:
            v_final_pts.append(self.game_json['instance']['gameDetails'][q])
        for q in hp:
            h_final_pts.append(self.game_json['instance']['gameDetails'][q])
        for total in totals_key_list:
            pts_total.append(self.game_json['instance']['gameDetails'][total])
        self.format_score_by_quarter(team_list[0], v_final_pts[0], v_final_pts[1], v_final_pts[2], v_final_pts[3],
                                     pts_total[0])
        self.format_score_by_quarter(team_list[1], h_final_pts[0], h_final_pts[1], h_final_pts[2], h_final_pts[3],
                                     pts_total[1])
        return

    # this is absolutely horrendous, but it works
    def fetch_box(self):
        keys = ['awayTeamStats', 'homeTeamStats']
        for key in keys:
            try:
                team = self.game_json['instance']['teamStats'][key][0]['team']['abbreviation']
                pens = self.game_json['instance']['teamStats'][key][0]['teamGameStats']['penaltiesTotal']
                rush_yds = self.game_json['instance']['teamStats'][key][0]['teamGameStats']['rushingYards']
                pass_yds = self.game_json['instance']['teamStats'][key][0]['teamGameStats']['passingNetYards']
                scrm_yds = self.game_json['instance']['teamStats'][key][0]['teamGameStats']['scrimmageYds']
                top = "{}:{}".format(int(str(float(self.game_json['instance']['teamStats'][key][0]['teamGameStats']
                                                   ['timeOfPossSeconds']) / 60).split(".")[0]),
                                     str(float(str(float(self.game_json['instance']['teamStats']['awayTeamStats'][0]
                                                         ['teamGameStats']['timeOfPossSeconds']) / 60)[:4]
                                               .split(".")[1]) * 6).split(".")[0])
                turnovers = "{}".format(int(self.game_json['instance']['teamStats'][key][0]
                                            ['teamGameStats']['passingInterceptions'])
                                        + int(self.game_json['instance']['teamStats'][key][0]
                                              ['teamGameStats']['fumblesLost']))
                self.format_box(team, pens, rush_yds, pass_yds, scrm_yds, top, turnovers)
            except IndexError:
                print("\nNo json data for box-stats yet...\n")
                continue
        return

    def get_title_info(self):
        date = ""
        game_time = ""
        teams_title = "#{} at {}\n\n".format(self.game_json['instance']['game']['awayTeam']['fullName'],
                                             self.game_json['instance']['game']['homeTeam']['fullName'])
        jd = json.loads(requests.get("https://feeds.nfl.com/feeds-rs/scores.json").text)
        for g in jd['gameScores']:
            if g['gameSchedule']['homeTeam']['nick'] .lower() == self.team or \
                    g['gameSchedule']['visitorTeam']['nick'].lower() == self.team:
                date = g['gameSchedule']['gameDate']
                game_time = g['gameSchedule']['gameTimeEastern']
        start_date = "{} {} Eastern".format(date, game_time)
        return "{}{}\n***".format(teams_title, start_date)

    def format_scoring_plays(self, team, q, play_type, desc):
        self.scoring_plays.append('\n| {} | {} | {} | {} |'.format(team, q, play_type, desc))

    def format_score_by_quarter(self, team, q1, q2, q3, q4, total):
        self.score_by_quarter.append("\n| {} | {} | {} | {} | {} | {} |".format(team, q1, q2, q3, q4, total))

    def format_box(self, team, penalties, rush_yds, net_pass_yds, scrm_yds, top, turnovers):
        self.box.append("\n| {} | {} | {} | {} | {} | {} | {} |".format(team, penalties, rush_yds, net_pass_yds,
                                                                        scrm_yds, top, turnovers))

    def build_pg_reply(self):
        reply = ""
        self.fetch_score_by_quarter()
        self.fetch_scoring_plays()
        self.fetch_box()
        reply += "\n{}\n".format(self.get_title_info())
        reply += "\n**Score by Quarter**\n"
        reply += self.sbq_header
        for s in self.score_by_quarter:
            reply += s
        reply += "\n**Scoring Plays**\n"
        reply += self.sp_header
        for s in self.scoring_plays:
            reply += s
        reply += "\n**Box Stats**\n"
        reply += self.box_header
        for s in self.box:
            reply += s
        print(reply)
        return reply
