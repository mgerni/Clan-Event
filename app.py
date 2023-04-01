from flask import Flask, render_template, request, session, redirect
from functools import wraps
import pymongo
from event import login_db, tasks_db, teams_db, clan_event, board, webhook
from time import sleep



app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecret'


MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)

db = db_client["ClanEvent"]
master_coll = db["MASTER"]
game_coll = db["GAME"]

team = None


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/event/admin/login/')
    return wrap


def event_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'team_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/event/login/')
    return wrap

@app.route('/')
def index():
    return redirect("event")

@app.route('/event/login/', methods=['GET', 'POST'])
def event_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_db.event_login(username, password, 'TEAMS'):
            session["team_logged_in"] = True
            session["team_username"] = username
            return redirect("/event/")
    return render_template('event_team_login.html')

@app.route('/event/')
@event_login_required
def event():
    if not len(clan_event.Team.instances):
        team = clan_event.Team(session['team_username'])
    else:
        team = clan_event.Team.instances[0]
        team.neighbors = list()
        team.travelled = list()
        team.update_attrs()
    teams = [ele for ele in teams_db.get_teams()]
    all_tiles = board.all_tiles
    return render_template("clan_event.html", all_tiles=all_tiles, teams=teams, current_team=team)

@app.route('/event/roll/')
@event_login_required
def team_roll():
    team = clan_event.Team.instances[0]
    if not team.roll_available:
        return redirect('/event/')
    #broadcast roll message?
    roll = team.team_roll()
    team.move_tiles(roll, team.current_tile)
    teams_db.update_team(team.username, {"current_tile": team.current_tile, 'roll_available': False})
    all_tiles = board.all_tiles
    print('Sending travelled list from event/roll: ', team.travelled)
    return render_template('clan_event_roll.html', all_tiles=all_tiles, current_team=team, roll=roll, travelled=team.travelled)


@app.route('/event/roll/choice/', methods=['POST'])
@event_login_required
def roll_choice():
    team = clan_event.Team.instances[0]
    if not team.roll_available:
        return redirect('/event/')
    all_tiles = board.all_tiles
    
    tile_index = request.form['tile_index']
    roll = request.form['roll']
    tile = all_tiles[int(tile_index)]
    return render_template('clan_event_roll_choice.html', all_tiles=all_tiles, tile=tile, current_team=team, roll=roll)


@app.route('/event/roll/complete/', methods=['POST'])
@event_login_required
def complete_roll():
    team = clan_event.Team.instances[0]
    if not team.roll_available:
        return redirect('/event/')
    all_tiles = board.all_tiles
    tile_index = request.form['tile_id']
    tile_index = int(tile_index)
    roll = request.form['roll']
    roll = int(roll)
    # 6 - 5 - 1 = 0
    remaining_roll = roll - len(team.travelled) - 1
    team.neighbors = list()
    team.travelled.append(tile_index)
    if all_tiles[tile_index]['type'] == 'O':
        print('do shop things2')
        remaining_roll += 1
    team.move_tiles(remaining_roll, tile_index)
    teams_db.update_team(team.username, {"current_tile": team.current_tile, 'roll_available': False})
    print('Sending travelled list from event/roll/choice: ', team.travelled)
    return render_template('roll_choice.html', all_tiles=all_tiles, current_team=team, roll=roll, travelled=team.travelled)



@app.route('/event/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_db.event_login(username, password, 'LOGIN'):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect("/event/admin/")
    return render_template('clan_event_admin_login.html')

@app.route('/event/logout/')
@event_login_required
def event_logout():
    clan_event.Team.instances = []
    session.clear()
    return redirect('/event/login')

@app.route('/event/admin/logout/')
@admin_required
def admin_logout():
    session.clear()
    return redirect('/event/admin/login/')


@app.route('/event/admin/', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    if request.method == 'POST':
        task_type, task_id, rate, divisor, coins, coinvalue = (request.form['type'], 
                                                               request.form['_id'], 
                                                               request.form['rate'], 
                                                               request.form['divisor'], 
                                                               request.form['coins'], 
                                                               request.form['coinvalue'])
        task_id = int(task_id)
        rate = int(rate)
        divisor = int(divisor)
        coins = int(coins)
        coinvalue = int(coinvalue)

        tasks_db.update_task(task_type, task_id, rate, divisor, coins, coinvalue)

    tasks = tasks_db.get_tasks()
    teams = teams_db.get_teams()
    return render_template('clan_event_admin_panel.html', tasks=tasks, teams=teams)


@app.route('/event/admin/add_team/', methods=['POST'])
@admin_required
def add_team():
    team_name = request.form['team_name']
    username = request.form['username']
    password = request.form['password']
    members = request.form['members'].split(',')
    teams_db.create_team(team_name, members, username, password)
    return redirect('/event/admin/')


@app.route('/event/task-complete/', methods=['POST'])
@event_login_required
def task_complete():
    print(request.form['name'])
    return redirect('/event/')

@app.route('/event/message/', methods=['POST'])
@event_login_required
def discord_message():
    team = clan_event.Team.instances[0]
    delay = request.form['delay']
    sleep(int(delay))
    # webhook.send_message(f"{team.username.capitalize()} {request.form['message']}")
    return 'just testing'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)