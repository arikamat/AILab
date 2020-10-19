from search_heuristics import *
from spotlessroomba_problem import *

INF = float('inf')

def spotlessroomba_first_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial admissible heuristic
    """
    Total Manhattan Distance
    Gives the roomba the ability to pass through walls and ignore additional cost on carpet
    1. Find closest dirty tile in manhattan distance
    2. Move roomba to closest dirty tile
    3. Repeat 1-2 until all dirty tiles are clean
    The heuristic is the total manhattan distance if the roomba moves to the closest dirty
    tile every time.
    """
    h = 0
    current_position = state.position
    dirty_locations = list(state.dirty_locations)
    lowest = INF
    closest_dirty = 0

    """for count in range(2):
        if not dirty_locations:
            return h
        for i in range(len(dirty_locations)):
            manhattan = abs(current_position.row - dirty_locations[i].row) + abs(current_position.col - dirty_locations[i].col)
            if manhattan < lowest:
                lowest = manhattan
                closest_dirty = i
        h += lowest
        current_position = dirty_locations.pop(closest_dirty)
        lowest = INF"""

    for i in range(len(dirty_locations)):
            manhattan = abs(current_position.row - dirty_locations[i].row) + abs(current_position.col - dirty_locations[i].col)
            lowest = min(lowest, manhattan)
            
    return lowest

def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial consistent heuristic
    best_path = [] # shortest order to visti all dirty tiles
    best_cost = INF # cost of above path

    # find shortest sequence of cleaning the dirty tiles
    for i in range(len(state.dirty_locations)):
        estimated_cost = 0
        lowest = INF
        closest_dirty = 0
        dirty_locations = list(state.dirty_locations)
        # set the start node and remove it from the list of nodes that have to be traveled to
        current_position = dirty_locations.pop(i)
        path = [current_position]
        
        while dirty_locations:
            for j in range(len(dirty_locations)):
                manhattan = abs(current_position.row - dirty_locations[j].row) + abs(current_position.col - dirty_locations[j].col)
                if manhattan < lowest:
                    lowest = manhattan
                    closest_dirty = j
            estimated_cost += lowest
            current_position = dirty_locations.pop(closest_dirty)
            path.append(current_position)
            lowest = INF
        if best_cost > estimated_cost:
            best_cost = estimated_cost
            best_path = path

    current_position = state.position
    # manhattan distance to next node in best_path
    manhattan_to_next_dirty = abs(current_position.row - best_path[0].row) + abs(current_position.row - best_path[0].col)
    return best_cost + manhattan_to_next_dirty


# Make sure to update names below, and add any extra you create.
SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Total Manhattan (admissible)": spotlessroomba_first_heuristic,
                        "Custom Heur. 2 (consistent)" : spotlessroomba_second_heuristic
                        }
