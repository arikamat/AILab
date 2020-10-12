# Lab 1, Part 2a: Heuristics.
# Name(s): 
from search_heuristics import *
from slidepuzzle_problem import *

INF = float('inf')

#### Lab 1, Part 2a: Heuristics #################################################

# Implement these two heuristic functions for SlidePuzzleState.

""" Return the Hamming distance (number of tiles out of place) of the SlidePuzzleState """
def slidepuzzle_hamming(state : SlidePuzzleState)  -> float:
    h = 0
    for row in range(state.get_size()):
        for col in range(state.get_size()):
            if state.tiles[row][col] != 0:
                if state.tiles[row][col] != row*state.get_size() + col:
                    h += 1
    return h

""" Return the sum of Manhattan distances between tiles and goal of the SlidePuzzleState """
def slidepuzzle_manhattan(state : SlidePuzzleState)  -> float:
    h = 0
    n = state.get_size()
    for row in range(n):
        for col in range(n):
            if state.tiles[row][col] != 0 and state.tiles[row][col] != row*n + col:
                h += abs(row - (state.tiles[row][col] // n)) + abs(col - (state.tiles[row][col] % n))
    return h

SLIDEPUZZLE_HEURISTICS = {
    "Zero" : zero_heuristic, 
    "Arbitrary": arbitrary_heuristic, 
    "Hamming" : slidepuzzle_hamming,
    "Manhattan" : slidepuzzle_manhattan
    }

