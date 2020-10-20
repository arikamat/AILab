# Lab 1, Part 2c: Heuristics.
# Name(s): Ari Kamat, Norikazu Kawasaki

from search_heuristics import *
from spotlessroomba_problem import *

INF = float('inf')

def spotlessroomba_first_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial admissible heuristic
    """
    Hamming Heuristic (admissible)
    provides very little speedup, but it's one line and admissible
    """
    return len(state.dirty_locations)


def spotlessroomba_second_heuristic(state : SpotlessRoombaState)  -> float:
    # TODO a nontrivial consistent heuristic
    """
    Best Path Heuristic (consistent)
    (seems to be a very good heuristic)
    Gives the roomba the ability to pass through walls and ignore additional cost on carpet
    1. Find which dirty tile is best to start from
        - For each dirty tile in state.dirty_locations
        1.1 Set it as the start node
        1.2 Use Total Manhattan Distance(third heuristic) to find route of least cost to visit every other dirty tile
        1.3 Compare with previous start tile, and keep the better start
            - (tiebreak with roomba proximity to start tile)
    2. Find roomba proximity to the best start tile
    3. Add the results of steps 1 and 2
    The heuristic is the sum of the distance to the best start tile and the cost from said tile
    """
    
    if not state.dirty_locations:
        return 0
    
    best_start = 0 # best dirty tile to start from
    best_cost = INF # cost of the path from the above start tile

    for i in range(len(state.dirty_locations)):
        estimate_cost = 0
        lowest_cost = INF
        closest_dirty = 0
        dirty_locations = list(state.dirty_locations)
        current_pos = dirty_locations.pop(i)

        # find the shortest cost solution path from this starting tile
        while dirty_locations:
            for j in range(len(dirty_locations)):
                manhattan = abs(current_pos.row - dirty_locations[j].row) + abs(current_pos.col - dirty_locations[j].col)
                if manhattan < lowest_cost:
                    lowest_cost = manhattan
                    closest_dirty = j
            estimate_cost += lowest_cost
            current_pos = dirty_locations.pop(closest_dirty)
            lowest_cost = INF
        # if estimated path cost is cheaper than best path cost so far, replace best_cost and best_start
        if estimate_cost < best_cost:
            best_cost = estimate_cost
            best_start = i
        # if estimated path cost and best path cost so far are equal, tiebreak with proximity to start tile
        if estimate_cost == best_cost:
            current_pos = state.position
            dist_to_prev_best = abs(current_pos.row - state.dirty_locations[best_start].row) + abs(current_pos.col - state.dirty_locations[best_start].col)
            dist_to_i = abs(current_pos.row - state.dirty_locations[i].row) + abs(current_pos.col - state.dirty_locations[i].col)
            if dist_to_i < dist_to_prev_best:
                best_start = i
    

    current_pos = state.position
    # Calculate distance to the best start tile
    dist_to_start = abs(current_pos.row - state.dirty_locations[best_start].row) + abs(current_pos.col - state.dirty_locations[best_start].col)
    # Returned heuristic is the sum of distance to the start tile and estimated cost from said tile
    return dist_to_start + best_cost


def spotlessroomba_third_heuristic(state : SpotlessRoombaState) -> float:
    """
    Total Manhattan Distance Heuristic (neither admissible nor consistent)
    (this heuristic is included moreso to show the idea Best Path is based, but it is
    often more effective than Hamming even if it isn't admissible)
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


# Make sure to update names below, and add any extra you create.
SPOTLESSROOMBA_HEURISTICS = {"Zero" : zero_heuristic,
                        "Arbitrary": arbitrary_heuristic, 
                        "Hamming (admissible)": spotlessroomba_first_heuristic,
                        "Best Path (consistent)" : spotlessroomba_second_heuristic,
                        "Total Manhattan (neither)" : spotlessroomba_third_heuristic
                        }
