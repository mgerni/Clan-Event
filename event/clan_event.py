from .board import all_tiles
import pymongo
from .teams_db import get_team_info, update_team
import random
from .webhook import send_embed_bank_passed



MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)


db = db_client['ClanEvent']
master_coll = db['MASTER']
game_coll = db['EVENT']

'''
Team Class:
    __init__():
        Class constructor, init instance of class:
            username: str - Username of the team
            team_info: dict - dict of MongoDB document of the team
            name: str - name of the team
            current_tile: int - Current tile team is on.
            members: list - List of team members names. 
            neighbors: list - list containing the neighbors for a board tile. will be used for when a tile requires choice.

    move_tiles():
        Class method, uses recursion to move the team through the board. 
            roll: int - Number of tiles to move. 
            start_index: int 

    update_db():
        Class method, update teams current_tile in database. NOT YET IMPLEMENTED. 
            team_id: int - id value for the team

    update_attrs():
        Class method, updates the attributes of the class instance from database.

    team_roll():
        Class method, rolls a random int between 1 and 10. 
'''
class Team:
    instances = []
    def __init__(self, username: str) -> None:
        self.__class__.instances.append(self)
        self.username = username
        self.team_info = get_team_info(self.username)
        self.neighbors = list()
        self.travelled = list()
        self.update_attrs()


    def move_tiles(self, roll: int, current_tile: int, manual_move: bool=False) -> list:
        if len(all_tiles[current_tile]['neighbor_list']) == 2:
            self.neighbors = all_tiles[current_tile]['neighbor_list']
            return

        else:
            self.travelled.append(all_tiles[current_tile]['neighbor_list'][0]['neighbor_id'])
            next_tile = all_tiles[current_tile]['neighbor_list'][0]['neighbor_id']
            
            if all_tiles[next_tile]['type'] == 'B' and roll > 1:
                print('Pay Money to bank', roll)
                self.current_tile = next_tile
                print(self.current_tile)
            
            elif all_tiles[next_tile]['type'] == 'B':
                print('Get money from bank', roll)
            
            elif all_tiles[next_tile]['type'] == 'X' and roll == 1:
                print('Do bowser things')
                self.current_tile = next_tile


            elif all_tiles[next_tile]['type'] == 'O':
                print('Do shop things')
                roll += 1
                
            if roll > 1:
                roll -= 1
                self.current_tile = next_tile
                self.move_tiles(roll, next_tile)
                

            elif roll == 1:
                self.current_tile = next_tile
            
            elif roll == 0:
                self.travelled.pop()
                self.current_tile = current_tile
            
 
    def update_attrs(self) -> None:
        
        self.team_info = get_team_info(self.username)
        self.coins = self.team_info['coins']
        self.total_coins = self.team_info['total_coins']
        self.skilling_minigames = self.team_info['Skilling Minigames']
        self.raids = self.team_info['Raids']
        self.slayer_bosses = self.team_info['Slayer bosses']
        self.slayer_uniques = self.team_info['Slayer uniques']
        self.monster_mash = self.team_info['Monster mash']
        self.wilderness = self.team_info['Wilderness']
        self.clues = self.team_info['Clues']
        self.godwars = self.team_info['God Wars dungeon']
        self.various_bosses = self.team_info['Various bosses']
        self.name = self.team_info['Name']
        self.current_tile = self.team_info['current_tile']
        self.coin_multiplier = self.team_info['coin_multiplier']
        self.roll_available = self.team_info['roll_available']
        self.shop_available = self.team_info['shop_available']
        self.bowser_available = self.team_info['bowser_available']
        self.members = self.team_info['members']

    def update_db(self, team_id: int) -> None:
        print('DO THE THING TO UPDATE THE DATABASE FOR THE TEAM')

    def team_roll(self) -> int:
        return random.choice(range(1, 11))


def get_event_status() -> dict:
    return game_coll.find_one({}, {'_id': 0,'frozen': 1})

def get_banked_coins() -> dict:
    return game_coll.find_one({}, {'_id': 0, 'bank_coins': 1})

def add_banked_coins(coins: int) -> None:
    game_coll.update_one({}, {'$set' : {'bank_coins': coins}})

if __name__ == '__main__':
    team = Team("team1")
    pass
    # team = Team(215, 'Team 1')
    # print(f'CURRENT TILE is: {team.current_tile}')
    # print(f'{team.name} ROLLED: 5!')
    # print(f'{team.name} Moves from [id: {team.current_tile}: type: {all_tiles[team.current_tile]["type"]}] to...')
    # team.move_tiles(5, team.current_tile)
    # print(f'TILE: [id: {team.current_tile}]: type: {all_tiles[team.current_tile]["type"]}')
    # team.update_db(0)


