import sqlite3
from bs4 import BeautifulSoup
from bs4 import Comment
from crawler import *

DBNAME = 'NBA_2017_18.db'


#this class use to match team for players, since the team name in player webpage in for short, so we just handle it here.
class check_team:
    def get_id(self, str):
        team_dict = {
            "GSW" : 1,
            "HOU" : 2,
            "NOP" : 3,
            "TOR" : 4,
            "CLE" : 5,
            "DEN" : 6,
            "PHI" : 7,
            "MIN" : 8,
            "LAC" : 9,
            "CHO" : 10,
            "LAL" : 11,
            "OKC" : 12,
            "WAS" : 13,
            "BRK" : 14,
            "MIL" : 15,
            "POR" : 16,
            "IND" : 17,
            "NYK" : 18,
            "UTA" : 19,
            "BOS" : 20,
            "PHO" : 21,
            "DET" : 22,
            "MIA" : 23,
            "ORL" : 24,
            "ATL" : 25,
            "CHI" : 26,
            "SAS" : 27,
            "DAL" : 28,
            "MEM" : 29,
            "SAC" : 30            
        }
        try:
            return team_dict[str]
        except:
            return None


def create_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # We have three tables in this project. Player, Team, Player_Team(many-to-many table).

    # Drop Table if needed
    statement = '''
        DROP TABLE IF EXISTS 'Player';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Team';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Player_Team';
    '''
    cur.execute(statement)

    conn.commit()

    # Create Table 'Player'
    statement = '''
        CREATE TABLE 'Player' (
           'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
           'Name' TEXT NOT NULL,
           'Position' TEXT NOT NULL,
           'Age' INTEGER NOT NULL
        )
    '''    
    cur.execute(statement)

    # Create Table 'Team'
    statement = '''
        CREATE TABLE 'Team' (
           'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
           'Name' TEXT NOT NULL,
           'Game' INTEGER NOT NULL,
           'Minute' REAL,
           'Field_Goal' REAL,
           'Field_Goal_Attempt' REAL,
           'Field_Goal_Percent' REAL,
           'Three_Field_Goal' REAL,
           'Three_Field_Goal_Attempt' REAL,
           'Three_Field_Goal_Percent' REAL,
           'Two_Field_Goal' REAL,
           'Two_Field_Goal_Attempt' REAL,
           'Two_Field_Goal_Percent' REAL,
           'Free_Throw' REAL,
           'Free_Throw_Attempt ' REAL,
           'Free_Throw_Percentage' REAL,
           'Offensive_Rebound' REAL,
           'Defensive_Rebound' REAL, 
           'Total_Rebound' REAL,
           'Assist' REAL,
           'Steal' REAL,
           'Block' REAL,
           'Turnover' REAL,
           'Personal_Foul' REAl,
           'Point' REAL
        )
    '''    
    cur.execute(statement)
    conn.commit()


    # Create Table "Player_Team"
    statement = '''
        CREATE TABLE 'Player_Team'(
           'Player_Id' INTEGER NOT NULL,
           'Team_Id' INTEGER NOT NULL,
           'Game' INTEGER NOT NULL,
           'Line_Up' INTERGER NOT NULL,
           'Minute' REAL,
           'Field_Goal' REAL,
           'Field_Goal_Attempt' REAL,
           'Field_Goal_Percent' REAL,
           'Three_Field_Goal' REAL,
           'Three_Field_Goal_Attempt' REAL,
           'Three_Field_Goal_Percent' REAL,
           'Two_Field_Goal' REAL,
           'Two_Field_Goal_Attempt' REAL,
           'Two_Field_Goal_Percent' REAL,
           'Effective_Field_Goal_Percent' REAL,
           'Free_Throw' REAL,
           'Free_Throw_Attempt ' REAL,
           'Free_Throw_Percentage' REAL,
           'Offensive_Rebound' REAL,
           'Defensive_Rebound' REAL, 
           'Total_Rebound' REAL,
           'Assist' REAL,
           'Steal' REAL,
           'Block' REAL,
           'Turnover' REAL,
           'Personal_Foul' REAl,
           'Point' REAL,
            FOREIGN KEY (Player_id) REFERENCES Player (Id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (Team_id) REFERENCES Team (Id) ON DELETE RESTRICT ON UPDATE CASCADE,
            PRIMARY KEY (Player_id, Team_id)                    
        )
    '''
    cur.execute(statement)
    conn.commit()

    conn.close()

def insert_Player_table_and_Player_Team_table():
    # I insert these two table together since they share the same source (nearly).
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    data = BeautifulSoup(get_data()[1], 'html.parser')
    table = data.find(class_ = "sortable stats_table")
    tbody = table.find("tbody")
    re = tbody.find_all("tr")
    getid = check_team()
    #check if the name to be inserted is unique
    namelist = []
    for i in re:
        if i['class'][0] != 'thead':
            # name = i.find("td").find("a").text
            rk = i.find(attrs={"data-stat": "ranker"}).text
            name = i.find(attrs={"data-stat": "player"}).text
            pos = i.find(attrs={"data-stat": "pos"}).text
            age = i.find(attrs={"data-stat": "age"}).text
            try:
                team = i.find(attrs={"data-stat": "team_id"}).find("a").text
            except:
                team = i.find(attrs={"data-stat": "team_id"}).text
            g = i.find(attrs={"data-stat": "g"}).text
            gs = i.find(attrs={"data-stat": "gs"}).text
            mp = i.find(attrs={"data-stat": "mp_per_g"}).text
            fg = i.find(attrs={"data-stat": "fg_per_g"}).text
            fga = i.find(attrs={"data-stat": "fga_per_g"}).text
            fgp = i.find(attrs={"data-stat": "fg_pct"}).text #it can be none
            three_fg = i.find(attrs={"data-stat": "fg3_per_g"}).text
            three_fga = i.find(attrs={"data-stat": "fg3a_per_g"}).text
            three_fgp = i.find(attrs={"data-stat": "fg3_pct"}).text
            two_fg = i.find(attrs={"data-stat": "fg2_per_g"}).text
            two_fga = i.find(attrs={"data-stat": "fg2a_per_g"}).text
            two_fgp = i.find(attrs={"data-stat": "fg2_pct"}).text
            efgp = i.find(attrs={"data-stat": "efg_pct"}).text
            ft = i.find(attrs={"data-stat": "ft_per_g"}).text
            fta = i.find(attrs={"data-stat": "fta_per_g"}).text
            ftp = i.find(attrs={"data-stat": "ft_pct"}).text
            orb = i.find(attrs={"data-stat": "orb_per_g"}).text
            drb = i.find(attrs={"data-stat": "drb_per_g"}).text
            trb = i.find(attrs={"data-stat": "trb_per_g"}).text
            ast = i.find(attrs={"data-stat": "ast_per_g"}).text
            stl = i.find(attrs={"data-stat": "stl_per_g"}).text
            blk = i.find(attrs={"data-stat": "blk_per_g"}).text
            tov = i.find(attrs={"data-stat": "tov_per_g"}).text
            pf = i.find(attrs={"data-stat": "pf_per_g"}).text
            pt = i.find(attrs={"data-stat": "pts_per_g"}).text        

            
            if name not in namelist:
                player = (None, name, pos, age)
                statement = 'INSERT INTO "Player" '  
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, player)
                namelist.append(name)
            
            player_id = namelist.index(name) + 1


            
            if team != "TOT":
                team_id = getid.get_id(team)

                player_team = (player_id, team_id, g, gs, mp, fg, fga, fgp, three_fg, three_fga, three_fgp, two_fg, two_fga, two_fgp, efgp, ft, fta, ftp, orb, drb, trb, ast, stl, blk, tov, pf, pt)
                statement_1 = 'INSERT INTO "Player_Team" '  
                statement_1 += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement_1, player_team)

    conn.commit()
    conn.close()  

def insert_Team_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    data = BeautifulSoup(get_data()[0], 'html.parser')
    # I find the table is under comment, so let's get data inside the comment, and do bs4 again.
    replace = ""
    comments=data.find_all(string=lambda text:isinstance(text,Comment))
    for comment in comments:
        tmp = "  <comment>{}</comment>  ".format(comment.strip())
        replace += tmp
    real_data = BeautifulSoup(replace, 'html.parser')
    table = real_data.find(class_= "sortable stats_table")
    tbody = table.find("tbody")
    re = tbody.find_all("tr")
    for i in re:
        rk = i.find(attrs={"data-stat": "ranker"}).text
        name = i.find(attrs={"data-stat": "team_name"}).text
        if name[-1:] == '*':
            name = name[:-2]
        g = i.find(attrs={"data-stat": "g"}).text
        mp = i.find(attrs={"data-stat": "mp"}).text
        fg = i.find(attrs={"data-stat": "fg"}).text
        fga = i.find(attrs={"data-stat": "fga"}).text
        fgp = i.find(attrs={"data-stat": "fg_pct"}).text
        three_fg = i.find(attrs={"data-stat": "fg3"}).text
        three_fga = i.find(attrs={"data-stat": "fg3a"}).text
        three_fgp = i.find(attrs={"data-stat": "fg3_pct"}).text
        two_fg = i.find(attrs={"data-stat": "fg2"}).text
        two_fga = i.find(attrs={"data-stat": "fg2a"}).text
        two_fgp = i.find(attrs={"data-stat": "fg2_pct"}).text
        ft = i.find(attrs={"data-stat": "ft"}).text
        fta = i.find(attrs={"data-stat": "fta"}).text
        ftp = i.find(attrs={"data-stat": "ft_pct"}).text
        orb = i.find(attrs={"data-stat": "orb"}).text
        drb = i.find(attrs={"data-stat": "drb"}).text
        trb = i.find(attrs={"data-stat": "trb"}).text
        ast = i.find(attrs={"data-stat": "ast"}).text
        stl = i.find(attrs={"data-stat": "stl"}).text
        blk = i.find(attrs={"data-stat": "blk"}).text
        tov = i.find(attrs={"data-stat": "tov"}).text
        pf = i.find(attrs={"data-stat": "pf"}).text
        pt = i.find(attrs={"data-stat": "pts"}).text        

        team = (None, name, g, mp, fg, fga, fgp, three_fg, three_fga, three_fgp, two_fg, two_fga, two_fgp, ft, fta, ftp, orb, drb, trb, ast, stl, blk, tov, pf, pt)
        # # we get player data, and now we insert the data into database
        statement = 'INSERT INTO "Team" '  
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, team) 
    conn.commit()
    conn.close()
