import json
from db import *
from datetime import datetime
# we have DBNAME in db.py and it's a global name

entries = []


def get_entries():
    global entries
    return entries

def get_part1_query(query_name):
    global entries
    entries = []
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    if query_name == "team":
        statement = '''
            SELECT Id, Name, Point, Total_Rebound, Assist, Steal, Block, Turnover,  Field_Goal, Field_Goal_Percent, Three_Field_Goal, Three_Field_Goal_Percent
            FROM Team
            ORDER BY Point DESC    
        '''
        cur.execute(statement)
        entries = cur.fetchall()
        return entries

    if query_name == "player":
        statement = '''
            SELECT Id, Name, Position, Age
            FROM Player
            ORDER BY Id
        '''
        cur.execute(statement)
        entries = cur.fetchall()
        return entries

    if query_name == "player_team":
        statement = '''
            SELECT p.Name, t.Name, pt.Game, pt.Line_Up, pt.Minute, pt.Point,pt.Total_Rebound, pt.Assist, pt.Steal, pt.Block, pt.Turnover, pt.Personal_Foul, pt.Field_Goal, pt.Field_Goal_Percent, pt.Three_Field_Goal, pt.Three_Field_Goal_Percent, pt.Effective_Field_Goal_Percent,
            pt.Free_Throw, pt.Free_Throw_Percentage

            FROM Player_Team AS pt
            LEFT JOIN Player AS p
            ON p.Id = pt.Player_Id
            LEFT JOIN Team AS t
            ON t.Id = pt.Team_Id
            ORDER BY pt.Point DESC
        '''
        cur.execute(statement)
        entries = cur.fetchall()
        return entries
    conn.close()
    return []


def get_part2_query(query_name):
    global entries
    entries = []
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    if query_name == "team":
        statement = '''
            SELECT Id, Name, Point, Total_Rebound, Assist, Steal, Block, Turnover,  Field_Goal, Field_Goal_Percent, Three_Field_Goal, Three_Field_Goal_Percent
            FROM Team
            ORDER BY Point DESC    
        '''
        cur.execute(statement)
        entries = cur.fetchall()
        return entries
    if query_name == "player":
        statement = '''
            SELECT p.Name, t.Name, pt.Game, pt.Line_Up, pt.Minute, pt.Point,pt.Total_Rebound, pt.Assist, pt.Steal, pt.Block, pt.Turnover, pt.Personal_Foul, pt.Field_Goal, pt.Field_Goal_Percent, pt.Three_Field_Goal, pt.Three_Field_Goal_Percent, pt.Effective_Field_Goal_Percent,
            pt.Free_Throw, pt.Free_Throw_Percentage

            FROM Player_Team AS pt
            LEFT JOIN Player AS p
            ON p.Id = pt.Player_Id
            LEFT JOIN Team AS t
            ON t.Id = pt.Team_Id
            ORDER BY pt.Point DESC
        '''
        cur.execute(statement)
        entries = cur.fetchall()
        return entries  
    conn.close()
    return []         

def get_player_in_team():
    global team_player
    team_player = {}
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Name FROM Team
    '''
    cur.execute(statement)
    team = cur.fetchall()
    team_cp =[]
    for i in team:
        team_cp.append(i[0])
    
    for i in team_cp:
        statement = '''
            SELECT p.Name FROM Player_Team AS pt
            LEFT JOIN Player AS p
            ON pt.Player_Id = p.Id
            LEFT JOIN Team AS t
            ON pt.Team_Id = t.Id
            WHERE t.Name = ?
        '''
        cur.execute(statement,(i,))
        sub_player = cur.fetchall()
        player_cp =[]
        for j in sub_player:
            player_cp.append(j[0])     
        team_player[i]=player_cp


    conn.close()
    return team_player, team_cp