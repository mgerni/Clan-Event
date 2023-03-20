from flask import Flask, render_template, request, session, redirect
import bcrypt
from functools import wraps
import pymongo 
from event.board import all_tiles
from event import login_db, tasks_db



app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"


MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)

db = db_client["ClanEvent"]
master_coll = db["MASTER"]
game_coll = db["GAME"]

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/event/admin/login/')
    return wrap

@app.route('/')
def index():
    return redirect("event")

@app.route('/event/')
def event():
    return render_template("clan_event.html", all_tiles=all_tiles)

@app.route('/event/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_db.admin_login(username, password):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect("/event/admin/")
    return render_template('clan_event_admin_login.html')


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
    return render_template("clan_event_admin_panel.html", tasks=tasks)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)