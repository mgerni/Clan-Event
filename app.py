from flask import Flask, render_template, request, session, redirect
from functools import wraps
import pymongo
from event import login_db, tasks_db, teams__db, clan_event, board




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
    teams = teams__db.get_teams()
    all_tiles = board.all_tiles
    return render_template("clan_event.html", all_tiles=all_tiles, teams=teams, current_team=team)


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
    teams = teams__db.get_teams()
    return render_template('clan_event_admin_panel.html', tasks=tasks, teams=teams)


@app.route('/event/admin/add_team/', methods=['POST'])
@admin_required
def add_team():
    team_name = request.form['team_name']
    username = request.form['username']
    password = request.form['password']
    members = request.form['members'].split(',')
    teams__db.create_team(team_name, members, username, password)
    return redirect('/event/admin/')


@app.route('/event/task-complete/', methods=['POST'])
@event_login_required
def task_complete():
    print(request.form['name'])
    return redirect('/event/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)