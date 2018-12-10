from main import *
import unittest

class Test_crawler(unittest.TestCase):
    def test_global_name(self):
        self.assertEqual(CACHE_NAME_1, 'team.json')
        self.assertEqual(CACHE_NAME_2, 'player.json')
    
    def test_get_data(self):
        tmp1, tmp2 = get_data()
        if not tmp1 or not tmp2:
            return False
        self.assertEqual(str(type(tmp1)), "<class 'str'>")
        self.assertEqual(str(type(tmp2)), "<class 'str'>")

        tmp3 = get_team_cache_data()
        self.assertNotEqual(tmp3, None)
        tmp4 = get_player_cache_data()
        self.assertNotEqual(tmp3, None)

class Test_database(unittest.TestCase):
    def test_global_name(self):
        self.assertEqual(DBNAME, 'NBA_2017_18.db')

    def test_check_team(self):
        tmp = check_team()
        self.assertEqual(tmp.get_id('BOS'),20)
        self.assertEqual(tmp.get_id('HOU'),2)
        self.assertEqual(tmp.get_id('MMM'),None)

    def test_create_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = "select * from {} ".format('Player') 
        cur.execute(sql)
        self.assertEqual([d[0] for d in cur.description], ['Id', 'Name', 'Position', 'Age'])
        
        sql = "select * from {} ".format('Player_Team') 
        cur.execute(sql)
        self.assertEqual(len([d[0] for d in cur.description]),27)

        sql = "select * from {} ".format('Team') 
        cur.execute(sql)
        self.assertEqual(len([d[0] for d in cur.description]),25)
        conn.close()

    def test_table_itself(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            select Name from Player
            where Name LIKE "%Paul"
        '''
        cur.execute(statement)
        tmp = cur.fetchall()
        self.assertEqual(len(tmp), 2)
        self.assertEqual(tmp[1][0], 'Chris Paul')   


        statement = '''
            select Name from Player
            where Age >= 40
        '''
        cur.execute(statement)
        tmp = cur.fetchall()
        self.assertEqual(len(tmp), 3)
        self.assertEqual(tmp[1][0], 'Manu Ginobili')  


        statement = '''
            select Name from Team
            where `Three_Field_Goal` >= 12
        '''
        cur.execute(statement)
        tmp = cur.fetchall()
        self.assertEqual(len(tmp), 3)
        self.assertEqual(tmp[0][0], 'Houston Rocket') 

        statement = '''
            select p.Name from Player as p
            left join Player_Team as pt
            on p.Id = pt.Player_Id
            left join Team as t
            on t.Id = pt.Team_Id
            where t.Name = "Houston Rocket"
        '''
        cur.execute(statement)
        tmp = cur.fetchall()
        self.assertEqual(len(tmp), 24)
        self.assertEqual(tmp[0][0], 'Ryan Anderson') 

        conn.close()

class Test_fontend(unittest.TestCase):
    def test_model_part1(self):
        data = get_part1_query("team")
        self.assertEqual(len(data),30)
        data = get_part1_query("player")
        self.assertEqual(len(data), 540)
        data = get_part1_query("player_team")
        self.assertEqual(len(data), 605)
    def test_model_part2(self):
        data = get_part2_query("team")
        self.assertEqual(len(data),30)
        data = get_part2_query("player")
        self.assertEqual(len(data), 605)
    def test_get_player_in_team(self):
        data = get_player_in_team()
        self.assertEqual(len(data[0]["Golden State Warrior"]), 17)
        self.assertEqual(len(data[1]), 30)
if __name__ == '__main__':
    unittest.main()
