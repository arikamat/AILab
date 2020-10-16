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
    partial_heuristic = INF
    closest_dirty = 0

    while dirty_locations:
        for i in range(len(dirty_locations)):
            manhattan = abs(current_position.row - dirty_locations[i].row) + abs(current_position.col - dirty_locations[i].col)
            if manhattan < partial_heuristic:
                partial_heuristic = manhattan
                closest_dirty = i
        h += partial_heuristic
        current_position = dirty_locations.pop(closest_dirty)
        partial_heuristic = INF
        
    return h

def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial consistent heuristic
    raise NotImplementedError

# Make sure to update names below, and add any extra you create.
SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Total Manhattan (admissible)": spotlessroomba_first_heuristic,
                        "Custom Heur. 2 (consistent)" : spotlessroomba_second_heuristic
                        }
