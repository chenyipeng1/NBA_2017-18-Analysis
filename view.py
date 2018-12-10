from flask import Flask, render_template, request, redirect
from model import *

app = Flask(__name__)

@app.route('/')
def welcome():
	    return render_template('index.html', entries=get_entries())

@app.route('/part1', methods=["POST"])
def make_decision_part1():
    query_name = request.form["part1_select"]
    if query_name == 'team':
        return render_template('team.html', entries=get_part1_query(query_name))
    if query_name == 'player':
        return render_template('player.html', entries=get_part1_query(query_name))     
    if query_name == 'player_team':
        return render_template('player_team.html', entries=get_part1_query(query_name))    

@app.route('/part2', methods=["POST"])
def make_decision_part2():
    query_name = request.form["part2_select"]
    if query_name == 'team':
        return render_template('compare_team.html', entries=get_part2_query(query_name), teams=get_player_in_team())
    if query_name == 'player':
        return render_template('compare_player.html', entries=get_part2_query(query_name), teams=get_player_in_team())      

@app.route('/rebuild_database', methods=["POST"])
def rebuild_database():
    create_table()
    insert_Player_table_and_Player_Team_table()
    insert_Team_table()
    return redirect('/')
