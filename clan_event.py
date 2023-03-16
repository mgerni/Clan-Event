from board import all_tiles

class Team:
    def __init__(self, current_tile: int, name: str) -> None:
        self.current_tile = current_tile
        self.name = name

    def move_tiles(self, roll: int, start_index: int) -> list:
        if roll != 0:
            if len(all_tiles[start_index]["neighbor_list"]) != 2:
                start_index = all_tiles[start_index]["neighbor_list"][0]["neighbor_id"]
                roll -= 1
                self.move_tiles(roll, start_index)
            neighbors = all_tiles[start_index]["neighbor|list"]
            return neighbors
            
        else:
            self.current_tile = start_index
        
    def update_db(self, team_id: int) -> None:
        print("DO THE THING TO UPDATE THE DATABASE FOR THE TEAM")


team = Team(215, "Team 1")

print(f"CURRENT TILE is: {team.current_tile}")
print(f"{team.name} ROLLED: 5!")
print(f"{team.name} Moves from [id: {team.current_tile}: type: {all_tiles[team.current_tile]['type']}] to...")
team.move_tiles(5, team.current_tile)
print(f"TILE: [id: {team.current_tile}]: type: {all_tiles[team.current_tile]['type']}")
team.update_db(0)