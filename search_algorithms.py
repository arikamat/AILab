# Lab 1, Part 2a & 2d: Heuristics.
# Name(s): Ari Kamat, Norikazu Kawasaki

from __future__ import annotations
from typing import List, Collection, Tuple, Callable, Optional, Union, Set, Dict, Type, Iterable
import random
from collections import deque
import heapq
from search_problem import StateNode, Action

INF = float('inf')

#### Lab 1, Part 1a: Uninformed Search #################################################

class GoalSearchAgent():
    """
    Abstract class for Goal Search Agents.
    """
    frontier : Collection[StateNode] # All Collections are "truthy" - they are True if not empty, False if empty
    total_extends : int 
    total_enqueues : int

    """ __init__, enqueue, and dequeue be overridden by STRATEGY partial subclasses (i.e. RandomSearch, DFS, BFS, UCS, Greedy, and AStar)"""

    def __init__(self, *args, **kwargs):
        """Initialize self.total_extends and self.total_enqueues to 0s. 
        Subclasses should initialize an empty frontier that enqueue() and dequeue() operate on.
        """
        super().__init__()
        self.total_extends = 0
        self.total_enqueues = 0

    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless some property (e.g. depth/path cost) exceeds the cutoff """
        # Subclasses will override and implement.
        raise NotImplementedError
        
    def dequeue(self) -> StateNode:
        """ Choose, remove, and return a state from the frontier """
        # Subclasses will override and implement.
        raise NotImplementedError

    """ search to be implemented by ALGORITHM partial subclasses (i.e. TreeSearch, GraphSearch, AnytimeSearch)"""

    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ To be overridden by algorithm subclasses (TreeSearchAgent, GraphSearchAgent, AnytimeSearchAlgorithm)
        Returns a StateNode representing a solution path to the goal state, or None if search failed.
        """
        raise NotImplementedError


class RandomSearch(GoalSearchAgent):
    """ Partial class representing the Random Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)
    """
    frontier : List[StateNode]
    
    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs) # pass any unused parameters to any superclasses
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        if state.depth < cutoff:
            self.frontier.append(state)

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return a random state from the frontier."""
        s = random.choice(self.frontier)
        self.frontier.remove(s)
        return s


class TreeSearchAlgorithm(GoalSearchAgent):
    """
    Mixin class for the tree search algorithm (without backtracking).

    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state. Here is the pseudocode:
        
        - Enqueue the initial_state in the frontier
        - Repeat while there are still StateNodes in the frontier:
            1) Dequeue a StateNode
            2) If the StateNode is a goal state, return it (end the search)
            3*) Call gui_callback_fn, passing it the dequeued StateNode. If it returns True, 
                end the search (the user has terminated early)
            4) Extend the dequeued state by enqueueing all its neighboring states. 
                - Implement the "no backtracking" optimization: do not enqueue parent states 
                - Pass the cutoff parameter to enqueue. 
                - Update self.total_extends and self.total_enqueues appropriately
        - If the search ends because the frontier is empty or gui_callback_fn ended the search
        early, return None.

        Remember that "tree search" may re-enqueue or re-extend the same state, multiple times.
        """

        #TODO implement!
        # enqueue initial state
        self.enqueue(initial_state, cutoff)
        self.total_enqueues += 1
        while len(self.frontier)>0:
            # dequeue node
            s = self.dequeue()
            # check if it is a goal state
            if s.is_goal_state():
               return s
            # extend node
            for action in s.get_all_actions():
                if gui_callback_fn(s):
                    return None
                a = s.get_next_state(action=action)
                if a != s.parent:
                    self.enqueue(a, cutoff)
                    self.total_enqueues += 1
            self.total_extends += 1
        return None


class DepthFirstSearch(GoalSearchAgent):
    """ Partial class representing the Depth First Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements search (i.e. TreeSearchAgent or GraphSearchAgent)

    DFS is implemented with a LIFO queue. A list is an efficient one. 
    """

    frontier : List[StateNode]

    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs)
        # TODO initiate frontier data structure
        self.total_extends = 0
        self.total_enqueues = 0
        self.frontier = []
        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        # TODO 
        if not state.depth > cutoff:
            self.frontier.append(state)
        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the MOST RECENTLY ADDED state from the frontier."""
        # TODO
        s = self.frontier.pop()
        return s

class BreadthFirstSearch(GoalSearchAgent):
    """ Partial class representing the Breadth First Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    BFS is implemented with a FIFO queue. 
    Lists are bad FIFO queues, but the deque data structure is an efficient implementation. 
    Check out the documentation of deque: https://docs.python.org/3/library/collections.html#collections.deque
    """
    frontier :Collection[StateNode]
    def __init__(self, *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs)
        self.total_extends=0
        self.total_enqueues=0
        self.frontier=[]
        # TODO initiate frontier data structure
        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless depth exceeds the cutoff """
        if not state.depth > cutoff: #state.depth<=cutoff
            self.frontier.append(state)
        

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the LEAST RECENTLY ADDED state from the frontier."""
        # TODO 
        choice = self.frontier.pop(0)
        return choice



class UniformCostSearch(GoalSearchAgent):
    """ Partial class representing the Uniform Cost Search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    UCS is implemented with a priority queue, which is typically a heap data structure. 
    The heapq library allows you to use a list as a efficient heap.
    (heapq.heappush and heapq.heappop are the main methods).
    Since states aren't ordered, the elements of the list-heap should be 
    tuples of (priority_value, statenode). heapq orders elements by the first element.

    Check out the documentation of heapq: https://docs.python.org/3/library/heapq.html
    """
    frontier : List[Tuple[float, StateNode]]
    
    def __init__(self,*args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        """
        super().__init__(*args, **kwargs)
        # TODO initiate frontier data structure
        self.total_extends = 0
        self.total_enqueues = 0
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
        # TODO 
        if not state.path_cost > cutoff:
            heapq.heappush(self.frontier, (state.path_cost, state))

        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with LOWEST PATH COST from the frontier."""
        # TODO 
        s = heapq.heappop(self.frontier)
        return s[1]


class GraphSearchAlgorithm(GoalSearchAgent):
    """
    Mixin class for the graph search (extended state filter) algorithm.
    
    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)

    When implementing a efficient filter, you'll want to use sets, not lists.
    Sets are like python dictionaries, except they only store keys (no values).
    The "in" keyword invokes a key lookup.
    Check out the documentation: https://docs.python.org/3/tutorial/datastructures.html#sets
    """
    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform a search from the initial_state, which constitutes the initial frontier.
        
        Graph search is similar to tree search, but it manages an "extended filter" 
        to avoid re-extending previously extended states again.

        Create a set of extended states. Before extending any state, check if the state has already been extended.
        If so, skip it. Otherwise, extend and add to the set. 
        """
        ext_filter : Set[StateNode] = set() # Create an empty extended state filter

        #TODO implement! (You may start by copying your TreeSearch's code)
        # enqueue initial state
        self.enqueue(initial_state, cutoff)
        self.total_enqueues += 1
        while self.frontier:
            # dequeue node
            s = self.dequeue()
            # extend node
            if s not in ext_filter:
                # check if it is a goal state
                if s.is_goal_state():
                    return s
                for action in s.get_all_actions():
                    if gui_callback_fn(s):
                        return None
                    if s.get_next_state(action) != s.parent:
                        self.enqueue(s.get_next_state(action), cutoff)
                        self.total_enqueues += 1
                self.total_extends += 1
                # temporary block to test admissibility
                try:
                    print(self.heuristic(s) + s.path_cost)
                except AttributeError:
                    pass
                ext_filter.add(s)
        return None




#### Lab 1, Part 2b: Informed Search #################################################

class InformedSearchAgent(GoalSearchAgent):
    """
    Abstract class for Informed Goal Search Agents.
    The only change from GoalSearchAgent is a cost-heuristic is provided
    at __init__, and will be used during search.
    """
    heuristic : Callable[[StateNode],float]

    def __init__(self, heuristic : Callable[[StateNode],float], *args, **kwargs):
        """ To be overridden by subclasses (RandomWalk, RandomSearch, DFS, BFS, UCS, Greedy, and AStar)
        Create an empty frontier queue, 
        and initialize self.total_extends and self.total_enqueues to 0s. 
        Will be called by GUI before any search.
        """
        super().__init__(heuristic = heuristic, *args, **kwargs) # pass any unused parameters to any superclasses
        self.heuristic = heuristic
    

class GreedyBestSearch(InformedSearchAgent):
    """ Partial class representing a search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    Greedy Best is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float]):
        """ Initialize self.total_extends and self.total_enqueues(done in super().__init__())
        Create an empty frontier queue.
        Also takes the heuristic function to be used as an estimate
        of the remaining cost to goal. 
        """
        super().__init__(heuristic)
        # TODO initiate frontier data structure
        self.total_extends=0
        self.total_enqueues=0
        self.frontier=[]

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
        if not state.path_cost >cutoff:
            self.frontier.append(state)
        

        
    def dequeue(self) -> Tuple[float, StateNode]:
        """  Choose and remove the state with LOWEST ESTIMATED REMAINING COST TO GOAL from the frontier."""
        sortedFrontier = sorted(self.frontier, key = self.heuristic)
        self.frontier.remove(sortedFrontier[0])
        return sortedFrontier[0]
    
class AStarSearch(InformedSearchAgent):
    """ Partial class representing a search strategy.
    To be subclassed (multiple inheritance) with a mixin that
    that implements a search algorithm (i.e. TreeSearchAgent or GraphSearchAgent)

    A* is implemented with a priority queue. 
    """
    frontier : List[Tuple[float, StateNode]]

    def __init__(self, heuristic : Callable[[StateNode],float], *args, **kwargs):
        """ Initialize self.total_extends and self.total_enqueues (done in super().__init__())
        Create an empty frontier queue.
        Also takes the heuristic function to be used as an estimate
        of remaining path cost. 
        """
        super().__init__(heuristic, *args, **kwargs)
        # TODO initiate frontier data structure
        self.total_extends = 0
        self.total_enqueues = 0
        self.frontier = []

        
    def enqueue(self, state: StateNode, cutoff: Union[int, float] = INF):
        """ Add the state to the frontier, unless path COST exceeds the cutoff """
       # TODO 
        if not state.path_cost > cutoff:
            heapq.heappush(self.frontier, (state.path_cost + self.heuristic(state), state))
        


        
    def dequeue(self) -> StateNode:
        """  Choose, remove, and return the state with LOWEST ESTIMATED TOTAL PATH COST from the frontier."""
        # TODO 
        s = heapq.heappop(self.frontier)
        return s[1]



""" Informed search algorithms can be reconfigured to provide a "closest" answer
if . This often happens because of early termination (by max length/cost cutoff or time limit).

The change is simple: during search, keep track of the state/path that is closest to the goal, 
according to the cost heuristic, and return it if the search ultimately fails/terminates early.
 
This is sometimes known as an "anytime" algorithm, because the algorithm can have at least
*some* useful result anytime the agent needs one.
"""

class AnytimeSearchAlgorithm(InformedSearchAgent):
    """
    Mixin class for "anytime" graph search algorithm.

    If terminating without finding the solution, returns the "best so far" solution with 
    the lowest estimated cost to goal, according to self.heuristic.
    
    Needs to be mixed in with a "strategy" subclass of GoalSearchAgent that
    implements the other methods (i.e. RandomSearch, DFS, BFS, UCS, etc.)
    """

    def search(self, 
            initial_state : StateNode, 
            gui_callback_fn : Callable[[StateNode],bool] = lambda : False,
            cutoff : Union[int, float] = INF 
            ) -> Optional[StateNode]:
        """ Perform an "Anytime" search from the initial_state

        This is the same as a graph search, but even if the search fails to find a solution, 
        it should always return the lowest-cost StateNode path  to the state closest* to the solution found so far.
        *Closest according to the agent's heuristic.
        """
        #TODO implement! (You may start by copying your GraphSearch's code)
        ext_filter : Set[StateNode] = set() # Create an empty extended state filter
        best_node = None
        best_heuristic = INF
        best_cost = INF


        # enqueue initial state
        self.enqueue(initial_state, cutoff)
        self.total_enqueues += 1
        while self.frontier:
            # dequeue node
            s = self.dequeue()
            # extend node
            if s not in ext_filter:
                # check if it is a goal state
                if s.is_goal_state():
                    return s
                # check if node is closer to goal           check if node is equally close but costs less
                if self.heuristic(s) < best_heuristic or (s.path_cost < best_cost and self.heuristic(s) == best_heuristic):
                    best_heuristic = self.heuristic(s)
                    best_cost = s.path_cost
                    best_node = s
                for action in s.get_all_actions():
                    if gui_callback_fn(s):
                        return best_node
                    if s.get_next_state(action) != s.parent:
                        self.enqueue(s.get_next_state(action), cutoff)
                        self.total_enqueues += 1
                self.total_extends += 1
                ext_filter.add(s)
        return best_node



# Collection of all the above. If you write other ones, add them here.

ALGORITHMS : Dict[str, Type[GoalSearchAgent] ] = {
    "tree": TreeSearchAlgorithm, 
    "graph": GraphSearchAlgorithm, 
    "anytime" : AnytimeSearchAlgorithm
}

STRATEGIES : Dict[str, Type[GoalSearchAgent] ] = {
    "random": RandomSearch,
    "dfs": DepthFirstSearch,
    "bfs": BreadthFirstSearch,
    "ucs": UniformCostSearch,
    "greedy": GreedyBestSearch,
    "astar": AStarSearch,
}

"""
Dynamically generate all class types that result from mixing the ALGORITHMS with the STRATEGIES
"""
ALL_AGENTS : Dict[str, Dict[str, Type[GoalSearchAgent] ]] = {}
for alg in ALGORITHMS:
    ALL_AGENTS[alg] = {}
    for strat in STRATEGIES:
        ALL_AGENTS[alg][strat] = type(alg + "-" + strat, (ALGORITHMS[alg], STRATEGIES[strat]), {})


### Completely Optional Extensions ########################################################

""" If you're bored, try any of the following extensions!
"""


""" A) Investigate a way to determine if a given slide puzzle is solvable without exhausting the whole state space.
 You may want to research the concept of parity. Implement is_solvable and make sure that it returns True on all the
 solvable test boards while returning False on the unsolvable ones.
 Write a script to open and test different slide puzzle boards.
 """

# from slidepuzzle_problem import SlidePuzzleState
# def is_solvable(board : SlidePuzzleState):
#     """is this board solvable? return a boolean"""
#     raise NotImplementedError


""" B) A* is optimal, but its memory usage is still prohibitive for large state spaces.
Investiate and implement one or more of the following: Recursive Best-First Search (RBFS), memory-bounded A* (MA*)
or simplified memory-bounded A* (SMA*).
"""


""" C) Improve upon these implementations! The framework given to you here
was designed to facilitate learning, not necessarily efficiency. 
There are many ways these algorithms can be improved in terms of speed and memory usage.
Furthermore, and problem-specific agents can usually take advantage of 
specific properties for even more efficiency. 
"""