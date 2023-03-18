import pymongo
import json
import bcrypt

MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)

db = db_client["ClanEvent"]
master_coll = db["MASTER"]
event_coll = db["EVENT"]
login_coll = db["LOGIN"]


def import_db(filename: str, collection: object) -> None:
    with open(filename) as f:
        data = json.load(f)
        del data[0]['_id']
        collection.insert_one(data[0])

if __name__ == '__main__':
    import_db('MASTER.json', master_coll)
    import_db('EVENT.json', event_coll)
    import_db('LOGIN.json', login_coll)


