from board import all_tiles
import pymongo
import db as taskdb


MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)

# mongo_uri = "mongodb+srv://taskapp-east.i78of.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

# db_client = pymongo.MongoClient(mongo_uri,
#                      tls=True,
#                      tlsCertificateKeyFile='X509-cert-7664155573852480772.pem')

db = db_client["ClanEvent"]
master_coll = db["MASTER"]
game_coll = db["GAME"]

'''
Team Class:
    __init__():
        Class contructor function, init instance of class:
            current_tile: int - Currernt tile team is on. Will be pulled from database in the end.
            name: str - name of the team
            neighbors: list - list containing the neighbors for a board tile. will be used for when a tile require choice.

    move_tiles():
        Class method, uses recursion to move the team through the board. 
            roll: int - Number of tiles to move. 
            start_index: int 

    update_db():
        Class method, update teams current_tile in database. NOT YET IMPLEMENTED. 
            team_id: int - id value for the team
'''
class Team:
    def __init__(self, current_tile: int, name: str) -> None:
        self.current_tile = current_tile
        self.name = name
        self.neighbors = list()

    def move_tiles(self, roll: int, start_index: int) -> list:
        if roll != 0:
            if len(all_tiles[start_index]["neighbor_list"]) != 2:
                start_index = all_tiles[start_index]["neighbor_list"][0]["neighbor_id"]
                roll -= 1
                self.move_tiles(roll, start_index)

            self.neighbors = all_tiles[start_index]["neighbor_list"]
            return
            
        else:
            self.current_tile = start_index
        
    def update_db(self, team_id: int) -> None:
        print("DO THE THING TO UPDATE THE DATABASE FOR THE TEAM")







if __name__ == "__main__":
    team = Team(215, "Team 1")
    print(f"CURRENT TILE is: {team.current_tile}")
    print(f"{team.name} ROLLED: 5!")
    print(f"{team.name} Moves from [id: {team.current_tile}: type: {all_tiles[team.current_tile]['type']}] to...")
    team.move_tiles(5, team.current_tile)
    print(f"TILE: [id: {team.current_tile}]: type: {all_tiles[team.current_tile]['type']}")
    team.update_db(0)


