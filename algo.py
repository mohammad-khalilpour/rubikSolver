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
        count = {'expanded': 0, 'explored': 0}

        def LDFS(state, limit):
            count.update({'expanded': count.get('expanded') + 1})
            if np.array_equal(state, solved_state()):
                return True

            if limit == 0:
                return False

            count.update({'explored': count.get('explored') + 12})
            for i in range(1, 13):
                if LDFS(next_state(state, i), limit - 1):
                    ans_list.append(i)
                    return True

            return False

        limit = 1
        while True:
            count.update({'explored': count.get('explored') + 1})
            if LDFS(init_state, limit):
                print("explored:" + str(count.get('explored')))
                print("expanded:" + str(count.get('expanded')))
                ans_list.reverse()
                return ans_list
            limit += 1

    elif method == 'A*':

        def calculate_heuristic(location):
            s_location = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
            heuristic = 0
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        heuristic += abs(x - s_location[location[z][y][x]-1][2]) + abs(y - s_location[location[z][y][x]-1][1]) + abs(z - s_location[location[z][y][x]-1][0])
            return heuristic / 4

        fringe = []
        visited = {}
        heapq.heappush(fringe, [calculate_heuristic(init_location), 0, 0, init_state, init_location, []])
        visited.update({init_state.__str__(): 0})
        expanded_count = 0
        explored_count = 0
        while True:
            forecasted_cost, current_cost, _, current_state, current_location, current_sol = heapq.heappop(fringe)
            expanded_count += 1
            if np.array_equal(current_state, solved_state()):
                break
            for i in range(1, 13):
                if next_state(current_state, i).__str__() not in visited.keys() or i < visited.get(next_state(current_state, i).__str__()):
                    explored_count += 1
                    visited.update({next_state(current_state, i).__str__(): current_cost + 1})
                    heapq.heappush(fringe, [current_cost + calculate_heuristic(next_location(current_location, i)) + 1, current_cost + 1, explored_count, next_state(current_state, i), next_location(current_location, i), np.append(current_sol, i)]),
        print("explored:" + str(explored_count))
        print("expanded:" + str(expanded_count))
        return current_sol

    elif method == 'BiBFS':
        source_fringe = []
        dest_fringe = []
        checked_source = {}
        checked_dest = {}

        checked_source.update({init_state.__str__(): []})
        checked_dest.update({solved_state().__str__(): []})
        source_fringe.append([init_state, []])
        dest_fringe.append([solved_state(), []])

        explored_count = 0
        expanded_count = 0
        while True:
            temp = source_fringe.copy()
            source_fringe.clear()

            for state in temp:
                expanded_count += 1
                current_state = state[0]
                current_sol = state[1]
                for i in range(1, 13):
                    explored_count += 1
                    n_state = next_state(current_state, i)
                    if n_state.__str__() in checked_dest:
                        t = checked_dest.get(n_state.__str__()).tolist()
                        t.reverse()
                        print("expanded nodes:" + str(expanded_count))
                        print("explored nodes:" + str(explored_count))
                        return np.append(np.append(current_sol, i), t)
                    if n_state.__str__() not in checked_source:
                        checked_source.update({n_state.__str__(): np.append(current_sol, i)})
                        source_fringe.append([n_state, np.append(current_sol, i)])

            temp = dest_fringe.copy()
            dest_fringe.clear()

            for state in temp:
                expanded_count += 1
                current_state = state[0]
                current_sol = state[1]
                for i in range(1, 13):
                    explored_count += 1
                    n_state = next_state(current_state, i)
                    q = (i + 6) % 12
                    if not q:
                        q = 12
                    if n_state.__str__() in checked_source:
                        t = np.append(current_sol, q).tolist()
                        t.reverse()
                        print("expanded nodes:" + str(expanded_count))
                        print("explored nodes:" + str(explored_count))
                        return np.append(checked_source.get(n_state.__str__()), t)
                    if n_state.__str__() not in checked_dest:
                        checked_dest.update({n_state.__str__(): np.append(current_sol, q)})
                        dest_fringe.append([n_state, np.append(current_sol, q)])

    else:
        return []
