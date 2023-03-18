from flask import Flask, render_template, request, session, redirect
import bcrypt
from functools import wraps
import pymongo 
from event.board import all_tiles



app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"


MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)

db = db_client["ClanEvent"]
master_coll = db["MASTER"]
game_coll = db["GAME"]

@app.route('/')
def index():
    return redirect("event")

@app.route('/event/')
def event():
    return render_template("clan_event.html", all_tiles=all_tiles)

@app.route('/event/admin/')
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        passsword = request.form['password']
    return render_template('clan_event_admin_login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)