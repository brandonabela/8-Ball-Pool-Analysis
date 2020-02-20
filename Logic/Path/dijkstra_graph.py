'''Dijkstra Graph'''

from collections import defaultdict

import math
import numpy as np


class DijkstraGraph:
    '''Responsible for handling dijkstra graph'''

    def __init__(self):
        '''Initiating a graph'''

        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        '''Adding an edge between two nodes'''

        to_node = (to_node[0], to_node[1])
        from_node = (from_node[0], from_node[1])

        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def find_any_goal_path(self, start, goals):
        '''Responsible for finding optimal path for any goal'''

        paths = []
        distances = []

        start = (start[0], start[1])
        goals = [(goal[0], goal[1]) for goal in goals]

        for goal in goals:
            path, distance = self.find_a_goal_path(start, goal)

            if distance != math.inf:
                paths.append(path)
                distances.append(distance)

        if paths:
            return paths[np.argmin(distances)]

        return []

    def find_a_goal_path(self, initial, end):
        '''Responsible for calculating the optimal path for a goal'''

        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = self.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = self.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return [], math.inf

            # Next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        path_weight = 0

        while current_node is not None:
            path.append(current_node)

            next_node = shortest_paths[current_node][0]
            path_weight += shortest_paths[current_node][1]

            current_node = next_node

        # Reverse path
        path = path[::-1]

        return path, path_weight
