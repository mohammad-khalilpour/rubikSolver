import heapq
import random

import numpy as np
from state import next_state, solved_state
from location import next_location, solved_location


def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == 'Random':
        return list(np.random.randint(1, 12+1, 10))

    elif method == 'IDS-DFS':
        ans_list = []

        def LDFS(state, limit):
            if np.array_equal(state, solved_state()):
                return True

            if limit == 0:
                return False

            for i in range(1, 13):
                if LDFS(next_state(state, i), limit - 1):
                    ans_list.append(i)
                    return True

            return False

        limit = 1
        while True:
            if LDFS(init_state, limit):
                ans_list.reverse()
                return ans_list
            limit += 1

    elif method == 'A*':

        def calculate_heuristic(location):
            heuristic = 0
            for x1 in range(2):
                for y1 in range(2):
                    for z1 in range(2):
                        for x2 in range(2):
                            for y2 in range(2):
                                for z2 in range(2):
                                    if solved_location()[z2][y2][x2] == location[z1][y1][x1]:
                                        heuristic += abs(z1 - z2) + abs(y2 - y1) + abs(x2 - x1)
            return heuristic / 4

        fringe = []
        visited = {}
        heapq.heappush(fringe, [calculate_heuristic(init_location), 0, 0, init_state, init_location, []])
        visited.update({init_state.__str__(): 0})
        count = 0
        while True:
            forecasted_cost, current_cost, _, current_state, current_location, current_sol = heapq.heappop(fringe)
            if np.array_equal(current_state, solved_state()):
                break
            for i in range(1, 13):
                if next_state(current_state, i).__str__() not in visited.keys() or i < visited.get(next_state(current_state, i).__str__()):
                    count += 1
                    visited.update({next_state(current_state, i).__str__(): current_cost + 1})
                    heapq.heappush(fringe, [current_cost + calculate_heuristic(next_location(current_location, i)) + 1, current_cost + 1, count, next_state(current_state, i), next_location(current_location, i), np.append(current_sol, i)]),

        return current_sol

    elif method == 'BiBFS':
        ...
    else:
        return []
