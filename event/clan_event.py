from .board import all_tiles
import pymongo
from .teams__db import get_team_info



MONGO_URI = 'mongodb://localhost:27017/'
db_client = pymongo.MongoClient(MONGO_URI)


db = db_client['ClanEvent']
master_coll = db['MASTER']
game_coll = db['GAME']

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
'''
class Team:
    instances = []
    def __init__(self, username: str) -> None:
        self.__class__.instances.append(self)
        self.username = username
        team_info = get_team_info(self.username)
        self.name = team_info['Name']
        self.current_tile = team_info['current_tile']
        self.coin_multiplier = team_info['coin_multiplier']
        self.members = team_info['members']
        self.neighbors = list()
        self.skilling_minigames = team_info['Skilling Minigames']
        self.raids = team_info['Raids']
        self.slayer_bosses = team_info['Slayer bosses']
        self.slayer_uniques = team_info['Slayer uniques']
        self.monster_mash = team_info['Monster mash']
        self.wilderness = team_info['Wilderness']
        self.clues = team_info['Clues']
        self.godwars = team_info['God Wars dungeon']
        self.various_bosses = team_info['Various bosses']

    def move_tiles(self, roll: int, start_index: int) -> list:
        if roll != 0:
            if len(all_tiles[start_index]['neighbor_list']) != 2:
                start_index = all_tiles[start_index]['neighbor_list'][0]['neighbor_id']
                roll -= 1
                self.move_tiles(roll, start_index)

            self.neighbors = all_tiles[start_index]['neighbor_list']
            return
            
        else:
            self.current_tile = start_index
        
    def update_db(self, team_id: int) -> None:
        print('DO THE THING TO UPDATE THE DATABASE FOR THE TEAM')






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


