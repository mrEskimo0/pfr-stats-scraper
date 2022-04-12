from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

#feed it desired url to scrape
def start_driver(url):
    PATH = '/Users/frankentwistle/desktop/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(7)
    return driver

def pfr_table_loop(draft_table, filters, d_columns):
    player_info = []
    
    #we need to skip first 2 iterations of the loop as they come back empty
    counter = 0
    for row in draft_table.find_elements_by_css_selector('tr'):
        if counter != 2:
            counter += 1
            continue
        else:
            row_info = []
            for cell in row.find_elements_by_tag_name('td'): 
                row_info.append(cell.text)
        
            
        #filt = what we are looking for aka filtering by, i_position is the index pos of the column
            print(row_info)
            for filt, i_position in filters.items():
                try:
                    if row_info[int(i_position)] == filt:
                        draft_info = []
                        mycols = d_columns[filt]
                        for index in mycols:
                            #pull info from table
                            draft_info.append(row_info[index])
                        player_info.append(draft_info)
                        print('player added')
                except IndexError:
                    print('shit the index was out of range')
                    continue
    print(player_info)
    return player_info   

#we want characters 49 to -4
def get_link(player_info, driver):
    player_links = []
    for playerlist in player_info:
        name = playerlist[1] 
        try:
            link = driver.find_element_by_link_text(name)
            time.sleep(.3)
            url = link.get_attribute('href')
            player_links.append(url)
            
        except:
            player_links.append('None')
            
    return player_links

def make_primary(player_info):
    split_names = [playerlist[1].split() for playerlist in player_info]
    primary_keys = []
    for name in split_names:
        new_key = name[0][0:2] + name[1][0:4]
        primary_keys.append(new_key)

#create player object to feed into database
# we want round, pick, name, position, school from table
#dat_id is database id or the primary key, we need to click the player name and get the snip of his url for prim key
class database_player:
    
    def __init__(self):
        self.player_id = ''
        self.position = ''
        self.pick = 0
        self.name = ''
        self.draft_school = ''
        self.link = ''
        self.draft_year = 0
        self.draft_round = 0