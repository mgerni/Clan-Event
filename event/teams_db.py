import pymongo
import bcrypt


MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)
db = db_client['ClanEvent']

master_coll = db['MASTER']
teams_coll = db["TEAMS"]


def create_team(name: str, members: list, username: str, password: str) -> None:
    copy_master = master_coll.find_one({'Name': 'MASTER'})
    del copy_master["_id"]
    new_team = copy_master
    new_team["Name"] = name
    for member in members:
        new_team["members"].append(member)
    new_team["username"] = username.lower()
    new_team["hash_pass"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    teams_coll.insert_one(new_team)

def get_team_info(username: str) -> dict:
    return teams_coll.find_one({'username': username}, {'_id': 0})

def get_teams() -> list: 
    return teams_coll.find({}, {'Name': 1, 'current_tile': 1, '_id': 0})

def update_team(team_name: str, update_dict: dict) -> None:
    teams_coll.update_one({"Name": team_name}, {'$set': update_dict})

def remove_coins_team(team_name: str, amount: int) -> None:
    current_coins = teams_coll.find_one({'Name': team_name}, {'_id': 0, 'coins': 1})
    teams_coll.update_one({'Name': team_name}, {'$set' : {'coins': current_coins['coins'] - amount}})
    
def add_coins_team(team_name: str, amount: int) -> None:
    current_coins = teams_coll.find_one({'Name': team_name}, {'_id': 0, 'coins': 1})
    teams_coll.update_one({'Name': team_name}, {'$set' : {'coins': current_coins["coins"] + amount}})

if __name__ == "__main__":
    # teams_coll.update_many({}, { '$set': {'shop_available': False, 'bowser_available': False, 'bank_available': False}})
    pass