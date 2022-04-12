#column problem
#for scoring, we need to look at column names for 2pt conversions as thats all we want from it
#receiving, rushing, passing, returns, we scrape
#tackles, def interceptions, we skip


def determine_columns(player_info, new_player):
    headers = {'Receiving':7, 'Rushing':4, 'Passing':11, 'Kick Returns':4, 
               'Punt Returns':4, 'Tackles':6, 'Fumbles':6, 'Def Interceptions':4, 'Punting':4, 'Scoring':2}
    
    passing = []
    rushing = []
    receiving = []
    punt_returns = []
    kick_returns = []
    fumbles = []
    twopoint = []
    intable_headers = player_info[0]
    column_names = player_info[1]
    x = 9
    
    if '2PM' in column_names:
        headers['Scoring'] = 3
    #account for fga and xpa as well
    
    for bucket in intable_headers:
        if bucket == 'Receiving':
            for y, game in enumerate(player_info):
                receiving_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    receiving_year.append('N')
                    receiving.append(receiving_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    try:
                        receiving_year.append(game[z+x])
                    except: #except the error for a non int
                        receiving_year.append(0)
                receiving.append(receiving_year)    
            x += headers[bucket]
            
        elif bucket == 'Rushing':
            for y, game in enumerate(player_info):
                rushing_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    rushing_year.append('N')
                    rushing.append(rushing_year)
                    continue
                for z in range(headers[bucket]):
                    rushing_year.append(game[z+x])
                rushing.append(rushing_year)
            x += headers[bucket]
                
        elif bucket == 'Passing':
            for y, game in enumerate(player_info):
                passing_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    passing_year.append('N')
                    passing.append(passing_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    passing_year.append(game[z+x])
                passing.append(passing_year)
            x += headers[bucket]
                
        elif bucket == 'Kick Returns':
            for y, game in enumerate(player_info):
                kick_returns_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    kick_returns_year.append('N')
                    kick_returns.append(kick_returns_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    kick_returns_year.append(game[z+x])
                kick_returns.append(kick_returns_year)
            x += headers[bucket]
                
        elif bucket == 'Punt Returns':
            for y, game in enumerate(player_info):
                punt_returns_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    punt_returns_year.append('N')
                    punt_returns.append(punt_returns_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    punt_returns_year.append(game[z+x])
                punt_returns.append(punt_returns_year)
            x += headers[bucket]
                
        elif bucket == 'Tackles':
            x += headers[bucket]
                
        elif bucket == 'Fumbles':
            for y, game in enumerate(player_info):
                fumbles_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    fumbles_year.append('N')
                    fumbles.append(fumbles_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    fumbles_year.append(game[z+x])
                fumbles.append(fumbles_year)
            x += headers[bucket]
                
        elif bucket == 'Def Interceptions':
            x += headers[bucket]
                
        elif bucket == 'Scoring' and headers['Scoring'] == 3:
            #only want 2pt conversions
            for y, game in enumerate(player_info):
                twopoint_year = []
                if y <= 1:
                    continue
                if len(game) < 15:
                    twopoint_year.append('N')
                    twopoint.append(twopoint_year)
                    #player didnt play, get game[-1] for reason and set everything to 0 or null
                    continue
                for z in range(headers[bucket]):
                    twopoint_year.append(game[x])
                twopoint.append(twopoint_year)
            x += headers[bucket]
            
        elif bucket == 'Scoring':
            x += headers[bucket]
        
    return passing, rushing, receiving, punt_returns, kick_returns, fumbles, twopoint

#get stats in game log page
def get_year_stats(driver):
    xpath = '//*[@id="stats"]'

    try:
        stats = driver.find_element_by_xpath(xpath)
    
    except NoSuchElementException:
        return "none"


    player_info = []
    for x, row in enumerate(stats.find_elements_by_css_selector('tr')):
        row_info = []
        if x <= 1:
            for cell in row.find_elements_by_tag_name('th'):
                row_info.append(cell.text)
            player_info.append(row_info)
            continue
        for cell in row.find_elements_by_tag_name('td'): 
            row_info.append(cell.text)
        player_info.append(row_info)
        
    return player_info

def search_bio(raw_info, position):

    info = []

    months = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September': '09',
              'October':'10', 'November':'11', 'December':'12'}

    raw_text = raw_info.text
    split_info = raw_text.split('\n')

    height = 0
    weight = 0
    birthday = '2020-01-01'
    feet_inches = 0
    actual_weight = 0
    converted_birthday = '2020-01-01'
    throw_hand = 'NA'

    if position == "QB":
        for x, i in enumerate(split_info):
            if re.search("Left|Right", i) and x < 3:
                throw_hand = re.search("Left|Right", i)
            if re.search("\d\d\dlb", i) and x < 4:
                weight = re.search("\d\d\dlb", i)
                height = re.search("\d-\d+", i)
            elif re.search("[^Born: ]\S+\s\d+,\s\d\d\d\d", i):
                birthday = re.search("[^Born: ]\S+\s\d+,\s\d\d\d\d", i)

    else:
        for i in split_info:
            if re.search("\d\d\dlb", i):
                weight = re.search("\d\d\dlb", i)
                height = re.search("\d-\d+", i)
            elif re.search("[^Born: ]\S+\s\d+,\s\d\d\d\d", i):
                birthday = re.search("[^Born: ]\S+\s\d+,\s\d\d\d\d", i)

    if height != 0:
        group = height.group()
        height_nohyp = group.split('-')
        feet = int(height_nohyp[0])
        inches = int(height_nohyp[1])
        feet_inches = (feet * 12) + inches

    if weight != 0:
        group_weight = weight.group()
        lbless_weight = group_weight.replace('lb', '')
        actual_weight = int(lbless_weight)

    if birthday != '2020-01-01':
        group_birthday = birthday.group()
        dob_spaces = group_birthday.replace(',', '')
        dob_split = dob_spaces.split(' ')
        converted_birthday = dob_split[2] + '-' + months[dob_split[0]] + '-' + dob_split[1]

    if position == 'QB':
        try:
            group_throwhand = throw_hand.group()
        except AttributeError:
            group_throwhand = 'NA'
        info.append(feet_inches)
        info.append(actual_weight)
        info.append(converted_birthday)
        info.append(group_throwhand)
    else:
        info.append(feet_inches)
        info.append(actual_weight)
        info.append(converted_birthday)
    return info


#start selenium webdriver
def start_driver(url):
    PATH = 'C:\\Users\\thelo_000\\Desktop\\chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(2)
    return driver

def main_table_scrape(driver, position, xpath_passing, xpath_rushrec, xpath_recrush):
    table_rows = []
    if position == 'QB':
        try:
            main_table = driver.find_element_by_xpath(xpath_passing)
            for row in main_table.find_elements_by_css_selector('tr'):
                table_rows.append(row.text)
            return table_rows, 'QB'
        except NoSuchElementException:
            print('QB does not have a passing table')
            return table_rows, 'QB'
        
        try:
            main_table = driver.find_element_by_xpath(xpath_rushrec)
            for row in main_table.find_elements_by_css_selector('tr'):
                table_rows.append(row.text)
            return table_rows, 'RB'
        except NoSuchElementException:
            pass
        try:
            main_table = driver.find_element_by_xpath(xpath_recrush)
            for row in main_table.find_elements_by_css_selector('tr'):
                table_rows.append(row.text)
            return table_rows, 'REC'
        except NoSuchElementException:
            print('no table for {}'.format(p_id))
            return table_rows
    else:
        try:
            main_table = driver.find_element_by_xpath(xpath_rushrec)
            for row in main_table.find_elements_by_css_selector('tr'):
                table_rows.append(row.text)
            return table_rows, 'RB'
        except NoSuchElementException:
            pass
        try:
            main_table = driver.find_element_by_xpath(xpath_recrush)
            for row in main_table.find_elements_by_css_selector('tr'):
                table_rows.append(row.text)
            return table_rows, 'REC'
        except NoSuchElementException:
            print('no table for {}'.format(p_id))
            return table_rows, 'REC'

def year_check(main_table, ps):
    split_rows = []
    years = []
    for row in main_table:
        split_rows.append(row.split())
    #remove the 2 header columns and summary column
    if ps != 'QB':
        split_rows.pop(0)
        split_rows.pop(0)
        split_rows.pop(-1)
    elif ps == 'QB':
        split_rows.pop(0)
        split_rows.pop(-1)
    for i in split_rows:
        years.append(i[0][0:4])
    return years

def standard_game_stats(player_info, year):
    year_stats = []
    for x, i in enumerate(player_info):
        game_stats = []
        if x <= 1:
            continue
        game_stats.append(year)
        game_stats.append(i[0])
        game_stats.append(int(i[1]))
        game_stats.append(int(i[2]))
        #do i put in the team number?
        game_stats.append(i[4])
        if i[5] == '@':
            game_stats.append('A')
        elif i[5] == '':
            game_stats.append('H')
        game_stats.append(i[6])
        #need to use regular expressions for home score, away score
        score = i[7][2:]
        split_score = score.split('-')
        game_stats.append(split_score[0])
        game_stats.append(split_score[1])
        if i[8] == '*':
            game_stats.append('Y')
        else:
            game_stats.append('N')
        
        if len(i) < 13:
            game_stats.append(0)
            game_stats.append(0)
        else:
            if int(year) > 2011:
                try:
                    game_stats.append(int(i[-5][:-1]))
                    game_stats.append(int(i[-6]))
                except ValueError:
                    game_stats.append(0)
                    game_stats.append(0)
            else:
                game_stats.append(0)
                game_stats.append(0)
        
        year_stats.append(game_stats)
    return year_stats

class core_stats:
    def __init__(self):
        self.throw_hand = 'N'
        self.height = 0
        self.weight = 0
        #datetime module here as well
        self.birthday = 'N'
        
class n_game:
    def __init__(self):
        self.did_play = 'Y'
        self.year = 0
        self.date = ''
        self.game_number = 0
        self.week = 0
        self.team = ''
        self.ishome = ''
        self.opponent = ''
        self.team_score = 0
        self.opp_score = 0
        self.starter = 'n'
        self.snaps_num = 0
        self.snaps_pct = 0
        #pass stats
        self.pass_att = 0
        self.pass_comp = 0
        self.cmp_pct = 0
        self.pass_yds = 0
        self.pass_td = 0
        self.ints = 0
        self.passer_rating = 0
        self.sacks = 0
        self.sack_yds = 0
        self.passyds_patt = 0
        self.adjyar_att = 0
        #rush stats
        self.rush_att = 0
        self.rush_yds = 0
        self.rushyds_patt = 0
        self.rush_tds = 0
        #receiving stats
        self.targets = 0
        self.receptions = 0
        self.rec_yards = 0
        self.yds_prec = 0
        self.rec_td = 0
        self.catch_pct = 0
        self.yds_ptar = 0
        #fumble stats
        self.fumbles = 0
        self.fumbles_lost = 0
        #return stats
        self.kick_returns = 0
        self.kick_returnyds = 0
        self.kick_ret_tds = 0
        self.punt_returns = 0
        self.punt_ret_yds = 0
        self.punt_ret_tds = 0
        #scoring
        self.twopointconvs = 0
        
        
class season:
    def __init__(self):
        self.year = ''
        #pass stats
        self.pass_att = 0
        self.pass_comp = 0
        self.cmp_pct = 0
        self.pass_yds = 0
        self.pass_td = 0
        self.ints = 0
        self.passer_rating = 0
        self.sacks = 0
        self.sack_yds = 0
        self.passyds_patt = 0
        self.adjyar_att = 0
        #rush stats
        self.rush_att = 0
        self.rush_yds = 0
        self.rushyds_patt = 0
        self.rush_tds = 0
        #receiving stats
        self.targets = 0
        self.receptions = 0
        self.rec_yards = 0
        self.yds_prec = 0
        self.rec_td = 0
        self.catch_pct = 0
        self.yds_ptar = 0
        #fumble stats
        self.fumbles = 0
        self.fumbles_lost = 0
        #return stats
        self.kick_returns = 0
        self.kick_returnyds = 0
        self.kick_ret_tds = 0
        self.punt_returns = 0
        self.punt_ret_yds = 0
        self.punt_ret_tds = 0
        #scoring
        self.twopointconvs = 0
        
class fantasy:
    def __init__(self):
        self.date = ''
        self.year = 0
        self.game_number = 0
        self.fantasy_pass_yds = 0
        self.fantasy_pass_tds = 0
        self.fantasy_pass_tds_six = 0
        self.fantasy_ints = 0
        self.fantasy_rush_yds = 0
        self.fantasy_rush_tds = 0
        self.fantasy_half_receptions = 0
        self.fantasy_full_receptions = 0
        self.fantasy_te_premium = 0
        self.fantasy_rec_yards = 0
        self.fantasy_rec_tds = 0
        self.fantasy_fumbles = 0
        self.fantasy_fumbles_lost = 0
        self.fantasy_twopointconvs = 0
        self.fantasy_returnyds = 0
        self.fantasy_returntds = 0
        
class fantasy_season:
    def __init__(self):
        self.year = 0
        self.fantasy_pass_yds = 0
        self.fantasy_pass_tds = 0
        self.fantasy_pass_tds_six = 0
        self.fantasy_ints = 0
        self.fantasy_rush_yds = 0
        self.fantasy_rush_tds = 0
        self.fantasy_half_receptions = 0
        self.fantasy_full_receptions = 0
        self.fantasy_te_premium = 0
        self.fantasy_rec_yards = 0
        self.fantasy_rec_tds = 0
        self.fantasy_fumbles = 0
        self.fantasy_fumbles_lost = 0
        self.fantasy_twopointconvs = 0
        self.fantasy_returnyds = 0
        self.fantasy_returntds = 0

def game_to_class(new_game, game):
    new_game.year = game[0]
    new_game.date = game[1]
    new_game.game_number = game[2]
    new_game.week = game[3]
    new_game.team = game[4]
    new_game.ishome = game[5]
    new_game.opponent = game[6]
    new_game.team_score = int(game[7])
    new_game.opp_score = int(game[8])
    new_game.starter = game[9]
    new_game.snaps_num = game[11]
    new_game.snaps_pct = game[10]

#log into database
def init_database(myhost, myuser, mypassword):
    try:
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
    except DatabaseError:
        time.sleep(20)
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

def update_player(p_id, mycursor, new_player):
    update_command = "UPDATE player set height=%s, weight=%s, dateofbirth=%s, throw_hand=%s WHERE id=%s"
    update_record = (new_player.height, new_player.weight, new_player.birthday, new_player.throw_hand, p_id)
    mycursor.execute(update_command, update_record)

def update_nonqb(p_id, mycursor, new_player):
    update_command = "UPDATE player set height=%s, weight=%s, dateofbirth=%s WHERE id=%s"
    update_record = (new_player.height, new_player.weight, new_player.birthday, p_id)
    mycursor.execute(update_command, update_record)

def insert_stats(p_id, mycursor, new_game):
    core_command = "INSERT into game_stats (playerid, year, gamedate, gamenumber, week, team, home, opponent, teamscore, oppscore, starter, didplay, snaps_num, snaps_pct, pass_att, pass_comp, cmp_pct, pass_yds, pass_td, ints, passer_rating, sacks, sack_yds, passyds_patt, adjyar_att, rush_att, rush_yds, rushyds_patt, rush_tds, targets, receptions, rec_yards, yds_prec, rec_td, catch_pct, yds_ptar, kick_returns, kick_returnyds, kick_ret_tds, punt_returns, punt_ret_yds, punt_ret_tds, fumbles, fumbles_lost, twopointconvs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    db_record_core = (p_id, new_game.year, new_game.date, new_game.game_number, new_game.week, new_game.team, new_game.ishome, new_game.opponent, new_game.team_score, new_game.opp_score, new_game.starter, new_game.did_play, new_game.snaps_num, new_game.snaps_pct, new_game.pass_att, new_game.pass_comp, new_game.cmp_pct, new_game.pass_yds, new_game.pass_td, new_game.ints, new_game.passer_rating, new_game.sacks, new_game.sack_yds, new_game.passyds_patt, new_game.adjyar_att, new_game.rush_att, new_game.rush_yds, new_game.rushyds_patt, new_game.rush_tds, new_game.targets, new_game.receptions, new_game.rec_yards, new_game.yds_prec, new_game.rec_td, new_game.catch_pct, new_game.yds_ptar, new_game.kick_returns, new_game.kick_returnyds, new_game.kick_ret_tds, new_game.punt_returns, new_game.punt_ret_yds, new_game.punt_ret_tds, new_game.fumbles, new_game.fumbles_lost, new_game.twopointconvs)
    try:
        mycursor.execute(core_command, (db_record_core))
    except mysql.connector.errors.IntegrityError:
        a, b, c = sys.exc_info()
        if b.errno == 1062:
            print('duplicate u dope')
        else:
            raise mysql.connector.errors.IntegrityError

def insert_stats_season(p_id, mycursor, season_stats):
    core_command_season = "INSERT into season_stats (playerid, year, pass_att, pass_comp, cmp_pct, pass_yds, pass_td, ints, passer_rating, sacks, sack_yds, passyds_patt, adjyar_att, rush_att, rush_yds, rushyds_patt, rush_tds, targets, receptions, rec_yards, yds_prec, rec_td, catch_pct, yds_ptar, kick_returns, kick_returnyds, kick_ret_tds, punt_returns, punt_ret_yds, punt_ret_tds, fumbles, fumbles_lost, twopointconvs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    db_record_core_season = (p_id, season_stats.year, season_stats.pass_att, season_stats.pass_comp, season_stats.cmp_pct, season_stats.pass_yds, season_stats.pass_td, season_stats.ints, season_stats.passer_rating, season_stats.sacks, season_stats.sack_yds, season_stats.passyds_patt, season_stats.adjyar_att, season_stats.rush_att, season_stats.rush_yds, season_stats.rushyds_patt, season_stats.rush_tds, season_stats.targets, season_stats.receptions, season_stats.rec_yards, season_stats.yds_prec, season_stats.rec_td, season_stats.catch_pct, season_stats.yds_ptar, season_stats.kick_returns, season_stats.kick_returnyds, season_stats.kick_ret_tds, season_stats.punt_returns, season_stats.punt_ret_yds, season_stats.punt_ret_tds, season_stats.fumbles, season_stats.fumbles_lost, season_stats.twopointconvs)
    try:
        mycursor.execute(core_command_season, (db_record_core_season))
    except mysql.connector.errors.IntegrityError:
        a, b, c = sys.exc_info()
        if b.errno == 1062:
            print('duplicate u dope')
        else:
            raise mysql.connector.errors.IntegrityError  

def insert_fantasy(p_id, mycursor, new_fantasy):
    fantasy_command = "INSERT into fantasy_stats_game (playerid, date, year, game_number, pass_yds_points, pass_tds_points, pass_tds_six_points, int_points, rush_yds_points, rush_tds_points, half_receptions_points, full_receptions_points, te_premium_points, rec_yards_points, rec_tds_points, fumbles_points, fumbles_lost_points, twopoint_convs_points, return_yards_points, return_tds_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    db_record_fantasy_game = (p_id, new_fantasy.date, new_fantasy.year, new_fantasy.game_number, new_fantasy.fantasy_pass_yds, new_fantasy.fantasy_pass_tds, new_fantasy.fantasy_pass_tds_six, new_fantasy.fantasy_ints, new_fantasy.fantasy_rush_yds, new_fantasy.fantasy_rush_tds, new_fantasy.fantasy_half_receptions, new_fantasy.fantasy_full_receptions, new_fantasy.fantasy_te_premium, new_fantasy.fantasy_rec_yards, new_fantasy.fantasy_rec_tds, new_fantasy.fantasy_fumbles, new_fantasy.fantasy_fumbles_lost, new_fantasy.fantasy_twopointconvs, new_fantasy.fantasy_returnyds, new_fantasy.fantasy_returntds)
    try:
        mycursor.execute(fantasy_command, (db_record_fantasy_game))
    except mysql.connector.errors.IntegrityError:
        a, b, c = sys.exc_info()
        if b.errno == 1062:
            print('duplicate u dope')
        else:
            raise mysql.connector.errors.IntegrityError

def insert_fantasy_season(p_id, mycursor, season_fantasy):
    fantasy_season_command = "INSERT into fantasy_stats_season (playerid, year, pass_yds_points, pass_tds_points, pass_tds_six_points, int_points, rush_yds_points, rush_tds_points, half_receptions_points, full_receptions_points, te_premium_points, rec_yards_points, rec_tds_points, fumbles_points, fumbles_lost_points, twopoint_convs_points, return_yards_points, return_tds_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    db_record_fantasy_game = (p_id, season_fantasy.year, season_fantasy.fantasy_pass_yds, season_fantasy.fantasy_pass_tds, season_fantasy.fantasy_pass_tds_six, season_fantasy.fantasy_ints, season_fantasy.fantasy_rush_yds, season_fantasy.fantasy_rush_tds, season_fantasy.fantasy_half_receptions, season_fantasy.fantasy_full_receptions, season_fantasy.fantasy_te_premium, season_fantasy.fantasy_rec_yards, season_fantasy.fantasy_rec_tds, season_fantasy.fantasy_fumbles, season_fantasy.fantasy_fumbles_lost, season_fantasy.fantasy_twopointconvs, season_fantasy.fantasy_returnyds, season_fantasy.fantasy_returntds)
    try:
        mycursor.execute(fantasy_season_command, (db_record_fantasy_game))
    except mysql.connector.errors.IntegrityError:
        a, b, c = sys.exc_info()
        if b.errno == 1062:
            print('duplicate u dope')
        else:
            raise mysql.connector.errors.IntegrityError



#START OF MAIN LOOP
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from mysql.connector import errorcode
from sys import exc_info
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from mysql.connector.errors import DatabaseError
import smtplib
from email_function import *
import sys
import time
import datetime
import re
import mysql.connector
import mysql

#global variables
myhost = 'JohnsNewPC'
myuser = 'franke'
mypassword = input('enter db password')
join_query = 'SELECT player.PFRlink, draft.draftyear, player.draftedposition, player.id FROM player INNER JOIN draft ON player.id=draft.playerid WHERE draft.draftyear < 2021 AND player.id > 145'
xpath_rushrec = '//*[@id="rushing_and_receiving"]'
xpath_recrush = '//*[@id="receiving_and_rushing"]'
xpath_passing = '//*[@id="passing"]'
stats_table = '//*[@id="stats"]'
t_input = input('enter app password')
password = 'ufalvkrljbpitz' + t_input

try:
    
    no_table_pids = []
    
    mycursor, db = init_database(myhost, myuser, mypassword)
    
    mycursor.execute(join_query)
    link_list = mycursor.fetchall()
    
    mycursor.close()
    
    
    print(link_list)
    
    for link, draft_year, position, p_id in link_list:
    
        #if link == no link skip    
        if link == 'None':
            continue
        #go to home page of player
        driver = start_driver(link)
        time.sleep(.5)
        #click expand info button to show DOB
        try:
            button = driver.find_element_by_xpath('//*[@id="meta_more_button"]')
            try:
                button.click()
            except ElementClickInterceptedException:
                driver.refresh()
        except NoSuchElementException:
            pass
        
        #isolate info text
        raw_info = driver.find_element_by_id('info')
        
        #use regular expressions to isolate throw hand, height, weight, DOB
        info = search_bio(raw_info, position)
        
        print(info)
        #make instance of class
        new_player = core_stats()
        new_player.height = info[0]
        new_player.weight = info[1]
        new_player.birthday = info[2]
        
        if position == 'QB':
            new_player.throw_hand = info[-1]
            mycursor = db.cursor()
            mycursor.execute("USE 3rdand20test")
            time.sleep(.1)
            update_player(p_id, mycursor, new_player)
            time.sleep(.1)
            db.commit()
            mycursor.close()
    
        
        else:
            mycursor = db.cursor()  
            mycursor.execute("USE 3rdand20test")
            update_nonqb(p_id, mycursor, new_player)
            time.sleep(.1)
            db.commit()
            mycursor.close()
    
    
        #get years from main table to scrape
        main_table, ps = main_table_scrape(driver, position, xpath_passing, xpath_rushrec, xpath_recrush)
        
        #if no main table then the player probably hasnt played, but i'll append them to a list to manually check
        if len(main_table) == 0:
            no_table_pids.append(p_id)
            driver.close()
            continue
        
        years = year_check(main_table, ps)
        
        #go to gamelog page for years that they have stats
        for year in years:
            #filter out non years
            if len(year) != 4:
                continue
            try:
                test_year = int(year)
            except ValueError:
                continue
            
            try:
                driver.get(link[:-4]+'/gamelog/'+year+'/')
    
            except (TimeoutException, WebDriverException) as e:
                driver.close()
                time.sleep(2)
                driver = start_driver(link[:-4]+'/gamelog/'+year+'/')
    
    
    
            #scrape per game stats table for the year
            player_info = get_year_stats(driver)
            print(player_info)
            
            if player_info == 'none':
                #insert year of 0s to indicate they didnt play
                season_stats = season()
                season_fantasy = fantasy_season()
                season_stats.year = year
                season_fantasy.year = year
                #shove
                mycursor = db.cursor()
                mycursor.execute("USE 3rdand20test")
                #shove
                insert_stats_season(p_id, mycursor, season_stats)
                insert_fantasy_season(p_id, mycursor, season_fantasy)
                
                #commit changes
                db.commit()
                print('commited a year')
                mycursor.close()    
                
                continue
                
            #get rid of summary row
            player_info.pop(-1)
            
            #get core stats from each game into a list
            core = standard_game_stats(player_info, year)
                
            #given buckets, get stats per game into lists
            passing, rushing, receiving, punt_returns, kick_returns, fumbles, twopoint  = determine_columns(player_info, new_player)
            
            season_stats = season()
            season_stats.year = year
            
            season_fantasy = fantasy_season()
            season_fantasy.year = year
            
            for x, week in enumerate(core):
                #put game stats into class instance
                new_game = n_game()
                
                new_fantasy = fantasy()
                new_fantasy.year = year
                
                #core stats into class
                game_to_class(new_game, week)
                
                #put date in fantasy_stats
                new_fantasy.date = new_game.date
                new_fantasy.game_number = new_game.game_number
                
                #put passing into class
                try:
                    if passing[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.pass_att = int(passing[x][1])
                        except ValueError:
                            pass
                        try:
                            new_game.pass_comp = int(passing[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.cmp_pct = float(passing[x][2])
                        except ValueError:
                            pass
                        try:
                            new_game.pass_yds = int(passing[x][3])
                        except ValueError:
                            pass
                        try:
                            new_game.pass_td = int(passing[x][4])
                        except ValueError:    
                            pass
                        try:
                            new_game.ints = int(passing[x][5])
                        except ValueError:
                            pass
                        try:
                            new_game.passer_rating = float(passing[x][6])
                        except ValueError:
                            pass
                        try:
                            new_game.sacks = int(passing[x][7])
                        except ValueError:
                            pass
                        try:
                            new_game.sack_yds = int(passing[x][8])
                        except ValueError:
                            pass
                        try:    
                            new_game.passyds_patt = float(passing[x][9])
                        except ValueError:
                            pass
                        try:
                            new_game.adjyar_att = float(passing[x][10])
                        except ValueError:
                            pass
    
                        new_fantasy.fantasy_pass_yds = new_game.pass_yds * .04
                        new_fantasy.fantasy_pass_tds = new_game.pass_td * 4
                        new_fantasy.fantasy_pass_tds_six = new_game.pass_td * 2
                        new_fantasy.fantasy_ints = new_game.ints * 2   
                        
                except IndexError:
                    pass
    
                #put rushing into class
                try: 
                    if rushing[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.rush_att = int(rushing[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.rush_yds = int(rushing[x][1])
                        except ValueError:
                            pass
                        try:
                            new_game.rushyds_patt = float(rushing[x][2])
                        except ValueError:
                            pass
                        try:
                            new_game.rush_tds = int(rushing[x][3])
                        except ValueError:
                            pass
    
                        new_fantasy.fantasy_rush_yds= new_game.rush_yds * .1
                        new_fantasy.fantasy_rush_tds = new_game.rush_tds * 6
                        
                except IndexError:
                    pass
                
                #put receiving into class
                try:
                    if receiving[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.targets = int(receiving[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.receptions = int(receiving[x][1])
                        except ValueError:
                            pass
                        try:
                            new_game.rec_yards = int(receiving[x][2])
                        except ValueError:
                            pass
                        try:
                            new_game.yds_prec = float(receiving[x][3])
                        except ValueError:
                            pass
                        try:
                            new_game.rec_td = int(receiving[x][4])
                        except ValueError:
                            pass
                        try:
                            new_game.catch_pct = float(receiving[x][5][:-1])
                        except ValueError:
                            pass
                        try:
                            new_game.yds_ptar = float(receiving[x][6])
                        except ValueError:
                            pass
    
                        new_fantasy.fantasy_half_receptions = new_game.receptions * .5
                        new_fantasy.fantasy_full_receptions = new_game.receptions
    
                        if position == 'TE':
                            new_fantasy.fantasy_te_premium = new_fantasy.fantasy_full_receptions * 1.5
                        else:
                            pass
    
                        new_fantasy.fantasy_rec_yards = new_game.rec_yards * .1
                        new_fantasy.fantasy_rec_tds = new_game.rec_td * 6
                        
                except IndexError:
                    pass
                
                #put punt returns into class
                try:
                    if punt_returns[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.punt_returns = int(punt_returns[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.punt_ret_yds = int(punt_returns[x][1])
                        except ValueError:
                            pass
                        try:
                            new_game.punt_ret_tds = int(punt_returns[x][3])
                        except ValueError:
                            pass
                
                
                
                
                        #fantasy return yards and tds
                        new_fantasy.fantasy_returnyds += round(new_game.punt_ret_yds / 25, 1)
                        new_fantasy.fantasy_returntds += (new_game.punt_ret_tds) * 6
                        
                except IndexError:
                    pass
                
                #put kick returns into classes
                try:
                    if kick_returns[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    
                        try:
                            new_game.kick_returns = int(kick_returns[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.kick_returnyds = int(kick_returns[x][1])
                        except ValueError:
                            pass
                        try:
                            new_game.kick_ret_tds = int(kick_returns[x][3])
                        except ValueError:
                            pass
                        
                        new_fantasy.fantasy_returnyds += round(new_game.kick_ret_yds / 25, 1)
                        new_fantasy.fantasy_returntds += (new_game.kick_ret_tds) * 6
                        
                except IndexError:
                    pass        
                
                #put fumbles into class
                try:
                    if fumbles[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.fumbles = int(fumbles[x][0])
                        except ValueError:
                            pass
                        try:
                            new_game.fumbles_lost = int(fumbles[x][1])
                        except ValueError:
                            pass
    
                        new_fantasy.fantasy_fumbles = new_game.fumbles
                        new_fantasy.fantasy_fumbles_lost = new_game.fumbles_lost * 2
                        
                except IndexError:
                    pass  
                
                #put 2pts in class
                try:
                    if twopoint[x][0] == 'N':
                        new_game.did_play = 'N'
                        pass
                    else:
                        try:
                            new_game.twopointconvs = int(twopoint[x][0])
                        except ValueError:
                            pass
    
                        new_fantasy.fantasy_twopointconvs = new_game.twopointconvs * 2
                
                except IndexError:
                    pass
                
                #fantasy leaderboard/summary per game
                new_fantasy.standard = new_fantasy.fantasy_pass_yds + new_fantasy.fantasy_pass_tds - new_fantasy.fantasy_ints + new_fantasy.fantasy_rush_yds + new_fantasy.fantasy_rush_tds + new_fantasy.fantasy_rec_yards + new_fantasy.fantasy_rec_tds - new_fantasy.fantasy_fumbles_lost + new_fantasy.fantasy_twopointconvs
                
                #sum up game stats for season stats
                #pass
                season_stats.pass_att += new_game.pass_att
                season_stats.pass_comp += new_game.pass_comp
                season_stats.pass_yds += new_game.pass_yds
                season_stats.pass_td += new_game.pass_td
                season_stats.ints += new_game.ints
                season_stats.sacks += new_game.sacks
                season_stats.sack_yds += new_game.sack_yds
                #rush
                season_stats.rush_att += new_game.rush_att
                season_stats.rush_yds += new_game.rush_yds
                season_stats.rush_tds += new_game.rush_tds
                #receiving
                season_stats.targets += new_game.targets
                season_stats.receptions += new_game.receptions
                season_stats.rec_yards += new_game.rec_yards
                season_stats.rec_td += new_game.rec_td
                #returns
                season_stats.kick_returns += new_game.kick_returns
                season_stats.kick_returnyds += new_game.kick_returnyds
                season_stats.kick_ret_tds += new_game.kick_ret_tds
                season_stats.punt_returns += new_game.punt_returns
                season_stats.punt_ret_yds += new_game.punt_ret_yds
                season_stats.punt_ret_tds += new_game.punt_ret_tds
                #fumbles
                season_stats.fumbles += new_game.fumbles
                season_stats.fumbles_lost += new_game.fumbles_lost
                #twopoint
                season_stats.twopointconvs += new_game.twopointconvs
                
                #add game stats to fantasy season stats
                season_fantasy.fantasy_pass_yds += new_fantasy.fantasy_pass_yds
                season_fantasy.fantasy_pass_tds += new_fantasy.fantasy_pass_tds
                season_fantasy.fantasy_pass_tds_six += new_fantasy.fantasy_pass_tds_six
                season_fantasy.fantasy_ints += new_fantasy.fantasy_ints
                season_fantasy.fantasy_rush_yds += new_fantasy.fantasy_rush_yds
                season_fantasy.fantasy_rush_tds += new_fantasy.fantasy_rush_tds
                season_fantasy.fantasy_half_receptions += new_fantasy.fantasy_half_receptions
                season_fantasy.fantasy_full_receptions += new_fantasy.fantasy_full_receptions
                season_fantasy.fantasy_te_premium += new_fantasy.fantasy_te_premium
                season_fantasy.fantasy_rec_yards += new_fantasy.fantasy_rec_yards
                season_fantasy.fantasy_rec_tds += new_fantasy.fantasy_rec_tds
                season_fantasy.fantasy_fumbles += new_fantasy.fantasy_fumbles
                season_fantasy.fantasy_fumbles_lost += new_fantasy.fantasy_fumbles_lost
                season_fantasy.fantasy_twopointconvs += new_fantasy.fantasy_twopointconvs
                season_fantasy.fantasy_returnyds += new_fantasy.fantasy_returnyds
                season_fantasy.fantasy_returntds += new_fantasy.fantasy_returntds
                
                #shove game stats + fantasy game stats into database
                mycursor = db.cursor()
                mycursor.execute("USE 3rdand20test")
                time.sleep(.5)
                
                insert_stats(p_id, mycursor, new_game)
                insert_fantasy(p_id, mycursor, new_fantasy)
                
                db.commit()
                time.sleep(.3)
                mycursor.close()
    
                
                del new_game
                del new_fantasy
                
            #calculate ratings for season stats
            try:
                season_stats.cmp_pct = round((season_stats.pass_comp / season_stats.pass_att) * 100, 2)
            except ZeroDivisionError:
                pass
            try:
                season_stats.passyds_patt = round(season_stats.pass_yds / season_stats.pass_att, 2)
            except ZeroDivisionError:
                pass
            try:
                adj_yar = (season_stats.pass_yds + 20 * season_stats.pass_td - 45 * season_stats.ints) / season_stats.pass_att
                season_stats.adjyar_att = round(adj_yar, 2)
            except ZeroDivisionError:
                pass
            try:
                a = (season_stats.pass_comp/season_stats.pass_att - .3) * 5
                b = (season_stats.pass_yds/season_stats.pass_att - 3) * .25
                c = (season_stats.pass_td / season_stats.pass_att) * 20
                d = 2.375 - (season_stats.ints/season_stats.pass_att * 25)
                passer_rating = ((a + b + c + d) / 6) * 100
                season_stats.passer_rating = round(passer_rating, 1)
            except ZeroDivisionError:
                pass
            try:
                season_stats.rushyds_patt = round(season_stats.rush_yds / season_stats.rush_att, 2)
            except ZeroDivisionError:
                pass
            try:
                season_stats.yds_prec = round(season_stats.rec_yards / season_stats.receptions, 2)
            except ZeroDivisionError:
                pass
            try:
                season_stats.catch_pct = round((season_stats.receptions / season_stats.targets) * 100, 2)
            except ZeroDivisionError:
                pass
            try:
                season_stats.yds_ptar = round(season_stats.rec_yards / season_stats.targets, 2)
            except ZeroDivisionError:
                pass
            
            mycursor = db.cursor()
            mycursor.execute("USE 3rdand20test")
            #shove
            insert_stats_season(p_id, mycursor, season_stats)
            insert_fantasy_season(p_id, mycursor, season_fantasy)
            
            #commit changes
            db.commit()
            print('commited a year')
            mycursor.close()
            
            
            
            
            #delete
            del season_stats
            del season_fantasy
    
        #close driver instance
        driver.close()

except Exception as e:
    print(e)
    error = str(e)
    email(error, password)