import mysql.connector
import mysql
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from mysql.connector import errorcode
from sys import exc_info
from draft_scrape_funcs import *

#globals
filters = {'QB':3, 'RB':3, 'WR':3, 'TE':3}
d_columns = {'QB':[0,2,3,4,26], 'RB':[0,2,3,4,26], 'WR':[0,2,3,4,26], 'TE':[0,2,3,4,26]}

myhost = 'JohnsNewPC'
myuser = 'franke'
mypassword = input('enter database password')

def init_database(myhost, myuser, mypassword):
    db = mysql.connector.connect(
    host= myhost,
    user= myuser,
    passwd= mypassword,
    auth_plugin= 'mysql_native_password',
    database= '3rdand20test'
    ) 
    mycursor = db.cursor()
    mycursor.execute("USE 3rdand20test")
    return mycursor, db

def database_push(mycursor, db, players_inclass):
    sql_command_player = "INSERT into Player (name, draftedposition, PFRlink) VALUES (%s, %s, %s)"
    sql_command_draft = "INSERT into Draft (playerid, DraftYear, DraftRound, DraftPick, School) VALUES (%s, %s, %s, %s, %s)" 
    for player in players_inclass:
        dbrecord_player = (player.name, player.position, player.link)
        dbrecord_draft = (player.draft_year, player.draft_round, player.pick, player.draft_school)
        try:
            mycursor.execute(sql_command_player, (dbrecord_player))
            last_id = mycursor.lastrowid
            mycursor.execute(sql_command_draft, (last_id,)+ dbrecord_draft)
        except mysql.connector.errors.IntegrityError:
            a, b, c = sys.exc_info()
            if b.errno == 1062:
                print('duplicate u dope')
                continue
            else:
                raise mysql.connector.errors.IntegrityError
    db.commit()
    time.sleep(.5)
    mycursor.close()
    time.sleep(.3)
    db.close()

def draft_round(player):
    pick = int(player[0])
    if pick < 33:
        drafted_round = 1
    elif pick > 32 and pick < 65:
        drafted_round = 2
    elif pick > 64 and pick < 102:
        drafted_round = 3
    elif pick > 101 and pick < 140:
        drafted_round = 4
    elif pick > 139 and pick < 177:
        drafted_round = 5
    elif pick > 176 and pick < 216:
        drafted_round = 6
    else:
        drafted_round = 7
    return drafted_round

# main loop
url = 'https://www.pro-football-reference.com/years/{}/draft.htm'

#loop thru years 2000 to 2020
#total_draft_players = []
for i in range(9,22):
    year = 2021 - i
    driver = start_driver(url.format(year))
    
    #isolate draft table in selenium
    draft_table = driver.find_element_by_id('drafts')

    player_info = pfr_table_loop(draft_table, filters, d_columns)

    player_links = get_link(player_info, driver)
    
    #player_keys = make_primary(player_info)
    
    for x, playerlist in enumerate(player_info):
        playerlist.append(player_links[x])
    
    players_inclass = []
    for player in player_info:  
        new_player = database_player()
        new_player.name = player[1]
        new_player.link = player[-2]
        new_player.position = player[2]
        new_player.pick = int(player[0])
        new_player.draft_school = player[4]
        new_player.player_id = player[-1]
        new_player.draft_year = year
        new_player.draft_round = draft_round(player)
        players_inclass.append(new_player)    
        
    #close driver
    driver.close()
    
    #start database
    mycursor, db = init_database(myhost, myuser, mypassword)
    
    #push players_inclass into database
    database_push(mycursor, db, players_inclass)
