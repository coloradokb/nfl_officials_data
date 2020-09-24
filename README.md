# nfl_officials_data
Simple scraping of web pages at www.pro-football-reference.com for officiating crew information

For purposes of tracking what officials (by name) and what crew(s) officated any given NFL regular season or playoff games. In-game data is limited to count of penalties enforced on the home and visiting team and the resulting yardage.

The data is sourced from pro-football-reference.com and each box score page for a game. For example, follow this link: https://www.pro-football-reference.com/boxscores/201909260gnb.htm

The officiating crew and their position as well as the yardage is on-page. 

Since there is no available api, BeautifulSoup via python3 is used to gather the data. This code makes no assumptions on how you collect the boxscores for each team per week per year. This is simply a tool to gather officiating crew(s) and the games they officated in the past.

*A note about not_given entries. There were changes to the Head Linesman went away in 2017. Some relics/old references in 2018/17. Must have to keep db/file sanity.
 Also, if the scraping grabbed but had issues locating the official by name, not_given might also be entered as a placeholder.
