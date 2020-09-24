import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class NFL_Officiating_Grabber:

    def __init__(self):
        pass

    def scrape_boxscore_pages(self, box_url_list):
        domain = 'https://www.pro-football-reference.com'
        for page in box_url_list:
            full_url = domain + page

            # definitely not efficient, but without creating new, clean object HTMLSession() would hang indefinitely after about 20-30 calls. Slows it down, but works
            session = HTMLSession()
            resp = session.get(full_url, timeout=30)
            resp.html.render()
            soup = BeautifulSoup(resp.html.html, 'lxml')
            session.close()
            time.sleep(5) #give the cleanup a few extra seconds
            return soup

    def officials_finder(self, officials_soup):
        game_crew_dict = {}
        game_crew_dict["Referee"]       = 'not_given'
        game_crew_dict["Umpire"]        = 'not_given'
        game_crew_dict["Down Judge"]    = 'not_given'
        game_crew_dict["Line Judge"]    = 'not_given'
        game_crew_dict["Side Judge"]    = 'not_given'
        game_crew_dict["Back Judge"]    = 'not_given'
        game_crew_dict["Field Judge"]   = 'not_given'
        game_crew_dict["Head Linesman"] = 'not_given'  # note...this went away in 2017. Some relics/old references in 2018/17. Must have to keep db sanity or other lookups
        try:
            for i, row in enumerate(officials_soup.find(id='all_officials')):
                if (i == 5):  # cutting to section to use - need to redo on text. static numbering is stupid is as stupid does
                    rows = BeautifulSoup(row, 'lxml')
                    for i, table_row in enumerate(rows.find_all('tr')[1:]):
                        ref_pos = table_row.find('th', attrs={'data-stat': 'ref_pos'}).text
                        ref_name = table_row.find('td', attrs={'data-stat': 'name'}).text
                        ref_name_arr = ref_name.split(' ')
                        f_name = ref_name_arr[0]
                        l_name = ref_name_arr[1]
                        ref_href = table_row.find('a')['href']
                        ref_href_arr = ref_href.split('/') # the id is array pos 3
                        #ref_unique_id = (ref_href_arr[2]).rstrip(".htm") #this is the pro-references unique identifier
                        #officials_table_id = 42 #this is a placeholder. having this value be a db lookup for existing officiating record is recommended
                        game_crew_dict[ref_pos] = f"{f_name} {l_name}"
        except Exception as e:
            print(f"ERR in officials_finder:\n   {e}")

        return (game_crew_dict)

    def find_penalties_data(self,soup):
        penalty_dict = {}
        penalties_soup = soup.find(id='div_team_stats')
        try:
            for i, row in enumerate(penalties_soup.find_all('tr')[2:]): #info starts at 2nd row
                if(row.find('th').text=='Penalties-Yards'):
                    vis_penalty = row.find('td', attrs={'data-stat': 'vis_stat'}).text.split('-')
                    home_penalty = row.find('td', attrs={'data-stat': 'home_stat'}).text.split('-')
                    penalty_dict['vis_count']  = vis_penalty[0]
                    penalty_dict['home_count'] = home_penalty[0]
                    penalty_dict['vis_yards']  = vis_penalty[1]
                    penalty_dict['home_yards'] = home_penalty[1]
        except Exception as e:
            print(f"ERR in find_penalties_data:\n   {e}")

        return(penalty_dict)

box_urls_list = {'/boxscores/201211250nor.htm'} #examples
obj              = NFL_Officiating_Grabber()
soup_page        = obj.scrape_boxscore_pages(box_urls_list)
officiating_crew = obj.officials_finder(soup_page)
print(officiating_crew)
penalty_data     = obj.find_penalties_data(soup_page)
print(penalty_data)