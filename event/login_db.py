import pymongo
import bcrypt

MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)
db = db_client["ClanEvent"]

login_coll = db["LOGIN"]

def admin_login(username, password):
    user_lookup = login_coll.find_one({"username": username})
    if user_lookup:
        hashed_pass = user_lookup["hash_pass"]
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, hashed_pass):
            return True
    return False