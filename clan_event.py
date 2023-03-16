from board import all_tiles
import csv

'''
Team Class:
    __init__():
        Class contructor function, init instance of class:
            current_tile: int - Currernt tile team is on. Will be pulled from database in the end.
            name: str - name of the team
            neighbors: list - list containing the neighbors for a board tile. will be used for when a tile require choice.
            tasklist: list - list of all the tasks and their completion state.
            coin_count: int - amount of coins owned by the team.
            star_count: int - amount of stars owned by the team.
            items_list: list - list of items owned by the team.
            next_task_coin_multiplier: int - multiplies the next task completion's coin reward.

    complete_task():
        Class method, marks a task as completed for the team and awards coins.
            task: str - name of the task that was completed.

    get_all_incomplete_tasks():
        Class method, returns all the tasks that aren't completed for the team.
    
    get_all_completed_tasks():
        Class method, returns all the tasks that are completed for the team.
    
    get_incomplete_tasks():
        Class method, returns the incomplete tasks for a specific category.
            category: str - name of the category.

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
        self.tasklist = list()
        self.coin_count = 0
        self.star_count = 0
        self.items_list = list()
        self.next_task_coin_multiplier = 1
        
        # The tasklist is in the format of [Category, Drop source, Task, Coinvalue, Completed]
        with open('taskList.csv', newline="") as csvfile:
            taskreader = csv.DictReader(csvfile, delimiter=",")
            for task in taskreader:
                self.tasklist.append([task["Category"],task['Drop source'],task['Task'],task['Coinvalue'], False])

    def complete_task(self, task: str) -> None:
        for entry in self.tasklist:
            if(entry[2] == task):
                entry[4] = True
                self.coin_count = self.coin_count + int(entry[3])*int(self.next_task_coin_multiplier)
                self.next_task_coin_multiplier = 1
                return
        print(f"Task not found: {task}")

    def get_all_incomplete_tasks(self) -> list:
        return list(filter(lambda task: task[4]==False, self.tasklist))

    def get_all_completed_tasks(self) -> list:
        return list(filter(lambda task: task[4]==True, self.tasklist))

    def get_incomplete_tasks(self, category: str) -> list:
        return list(filter(lambda task: task[0]==category and task[4]==False, self.tasklist))

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

    print(f"Team coins: {team.coin_count}")
    team.complete_task("Green dye")
    print(f"Team coins: {team.coin_count}")
    team.next_task_coin_multiplier = 3
    team.complete_task("Red dye")
    print(f"Team coins: {team.coin_count}")
    team.complete_task("Blue dye")
    print(f"Team coins: {team.coin_count}")
    print(team.get_all_completed_tasks())