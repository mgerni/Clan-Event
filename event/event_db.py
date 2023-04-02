import pymongo 

MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)
db = db_client['ClanEvent']

event_coll = db['EVENT']


def get_event_status() -> dict:
    return event_coll.find_one({'id': 'event_state'}, {'_id': 0,'frozen': 1})

def get_bank_value() -> dict:
    return event_coll.find_one({'id': 'event_state'}, {'_id': 0, 'bank_coins': 1})

def add_to_bank(amount: int) -> None:
    bank_value = get_bank_value()
    bank_value['bank_coins'] += amount
    event_coll.update_one({'id': 'event_state'}, {'$set' : {'bank_coins': bank_value['bank_coins']}})

def remove_coins_bank() -> None:
    event_coll.update_one({'id': 'event_state'}, {'$set' : {'bank_coins': 0}})
    
    
if __name__ == '__main__':
    x = get_bank_value()
    print(x)