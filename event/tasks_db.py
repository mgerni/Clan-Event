import pymongo

MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)
db = db_client["ClanEvent"]

master_coll = db["MASTER"]


def get_tasks():
    return master_coll.find_one(
            {
                "Name": "MASTER"
            }, 
            {
                "_id": 0,
                "Skilling Minigames" : 1,
                "Raids" : 1,
                "Slayer bosses" : 1,
                "Slayer uniques" : 1,
                "Monster mash": 1,
                "Wilderness" : 1,
                "Clues" : 1,
                "God Wars dungeon" : 1,
                "Various bosses" : 1
            }
        )

def update_task(task_type, task_id, rate, divisor, coins, coinvalue):
    master_coll.update_one({"Name": "MASTER", f"{task_type}._id" : task_id}, 
                  {"$set": 
                    {
                        f"{task_type}.$.rate" : rate,
                        f"{task_type}.$.divisor": divisor,
                        f"{task_type}.$.coins" : coins,
                        f"{task_type}.$.coinvalue" : coinvalue,
                     }})