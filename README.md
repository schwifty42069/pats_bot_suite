## The [r/Patriots](https://reddit.com/r/patriots) Utility Bot Suite
***
*The [PatsUtilityBot](https://reddit.com/user/PatsUtilityBot) suite is a series of article scraping and comment/submission reply bots
all rolled into a single module. Below you will find the basic details of it's functionality at this
point in time (as the bot is still actively being developed).*

## **Article Submission Scraping**
***
The bot can identify/scrape and reply with formatted articles from the following websites:

* **NESN**

* **PatsPulpit**

* **PatriotsWire**

* **WEEI**

*More detailed information on the implementation of the scrapers can be found in the docstrings
within the module itself.*
***
## **Comment Reply Functions**
***
*The bot can reply to a series of comment initiated commands/keywords. These currently include the following:*

* **!slater** - Replies with "Awwwwww Yeahhhhhhh!" (A long-standing Patriots locker room victory tradition, lead by Matthew Slater).

* **!refs** - Replies with "Fuck the Refs!" (Used primarily during games to express dissatisfaction with a call on the field).

* **jets** - Anytime the word "jets" appears in a comment, the bot replies with "Fuck the Jets" (An expression of the 
AFCE "rivalry" between the two teams).

* **!boohoo** - Replies with "Boohoo! My team wost to da patwiots! D:" (Used primarily when fans of a team the Patriots
have just defeated come and trash talk in a thread).
***
## **Post-Game Stats Scraping**
***
*After each game, an official post-game thread is posted by the mods. These threads tend to lack the box-score/stats and
score by quarter. To make up for this, the bot searches for the official post-game thread by submission  and automatically
replies with the post-game stats formatted into pretty markdown tables. Details of the implementation can be found in the
docstrings within the module itself. Below is an example of the formatted reply:*


#Dallas Cowboys at New England Patriots

11/24/2019 16:25:00 Eastern
***


**Score by Quarter**

| Team  | Q1 | Q2 | Q3 | Q4 | Total | 
| ------|----|----|----|----|-------|
| Cowboys | 0 | 6 | 0 | 3 | 9 |
| Patriots | 7 | 3 | 0 | 3 | 13 |


**Scoring Plays**

| Team | Quarter | Type | Description |
|------|---------|------|-------------|
| Patriots | 1 | TD | (:50) (Shotgun) T.Brady pass short left to N.Harry for 10 yards, TOUCHDOWN. NE 12-Brady 75th different career TD target, extends NFL record (Testaverde 70). NE 12-Brady 15th of season, NFL record for player after their 42nd birthday. |
| Patriots | 2 | FG | (12:51) N.Folk 44 yard field goal is GOOD, Center-J.Cardona, Holder-J.Bailey. |
| Cowboys | 2 | FG | (8:40) B.Maher 46 yard field goal is GOOD, Center-L.Ladouceur, Holder-C.Jones. |
| Cowboys | 2 | FG | (2:31) B.Maher 27 yard field goal is GOOD, Center-L.Ladouceur, Holder-C.Jones. |
| Patriots | 4 | FG | (9:37) N.Folk 42 yard field goal is GOOD, Center-J.Cardona, Holder-J.Bailey. NE 9-Folk 1,101 career pts, 49th all-time. |
| Cowboys | 4 | FG | (6:08) B.Maher 29 yard field goal is GOOD, Center-L.Ladouceur, Holder-C.Jones. |

**Box Stats**

| Team | Penalties | Rushing Yards | Net Passing Yards | Scrim. Yards| Time of Possession | Turnovers |
|------|-----------|---------------|-------------------|-------------|--------------------|-----------|
| DAL | 7 | 109 | 199 | 308 | 30:18 | 1 |
| NE | 6 | 101 | 181 | 282 | 29:18 | 0 |
***
## **In The Works**
***
*The following are additional functionality that will be added to the bot in time*:

* Specific stat scraping via comment command syntax

* Additional sources for article scraping

* Patriots.com video isolation and encoding (from m3u8 to mp4).

***
*If you have any questions, or wish to contribute to the bot, click [here](https://www.reddit.com/message/compose/?to=apt-get-schwifty)
to message me on reddit, or feel free to reach out to me here on github!*
