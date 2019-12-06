'''Ball Path Finding Handling Module'''

import math
import itertools
import numpy as np

import Config.eight_ball_lookup as lookup

from Logic.ball_colour import BallColour
from Logic.dijkstra_graph import DijkstraGraph

class BallPath:
    ''' Responsible for finding an optimal path '''

    min_angle = 40
    max_angle = 300

    def find_path(self, balls, holes, ball_colour, hit_number):
        '''Responsible for calculating an optimal path for a number of hits'''

        white_index = self.get_balls_index(balls, BallColour.White)
        target_indexes = self.get_balls_index(balls, ball_colour)

        if (balls and holes and white_index and target_indexes and not white_index in target_indexes):
            graph = DijkstraGraph()

            self.add_graph_edges(graph, balls, holes, ball_colour, hit_number)

            return graph.find_any_goal_path(white_index, range(len(balls), len(balls) + len(holes)))

        return []

    def find_valid_hit(self, balls, holes, ball_colour):
        '''Responsible for finding an optimal path while considering the walls'''

        sorted_holes = sorted(holes, key=lambda tup: (-tup[1], tup[0]))
        sorted_holes[2::] = sorted_holes[3::-1]

        all_objects = balls + sorted_holes

        white_index = self.get_balls_index(balls, BallColour.White)
        target_indexes = self.get_balls_index(balls, ball_colour)

        if (balls and holes and white_index and target_indexes and not white_index in target_indexes):
            for i, _ in enumerate(sorted_holes[:-1]):
                for target_index in target_indexes:
                    side_point = self.find_side_position(sorted_holes[i], sorted_holes[i + 1], all_objects[white_index], all_objects[target_index])

                    if side_point is not None:
                        is_start_valid = self.is_path_ocluded(all_objects[white_index], side_point, [white_index], all_objects)
                        is_end_valid = self.is_path_ocluded(side_point, all_objects[target_index], [target_index], all_objects)

                        if is_start_valid and is_end_valid:
                            angle = self.angle_between_three_points(all_objects[white_index], side_point, all_objects[target_index])

                            if self.min_angle < angle < self.max_angle:
                                return [white_index, side_point, target_index]

            graph = DijkstraGraph()
            self.add_graph_edges(graph, balls, sorted_holes, ball_colour, 1)
            return graph.find_any_goal_path(white_index, target_indexes)

        return []

    def find_side_position(self, hole_current, hole_next, start_ball, end_ball):
        '''Responsible for finding a mid point for a board side'''

        side_point = None

        is_x_axis_line = hole_current[0] == hole_next[0]
        is_y_axis_line = hole_current[1] == hole_next[1]

        mid_point = self.mid_point_from_two_points(start_ball, end_ball)

        if is_x_axis_line:
            side_point = (hole_current[0], int(mid_point[1]))

        if is_y_axis_line:
            side_point = (int(mid_point[0]), hole_current[1])

        return side_point

    def add_graph_edges(self, graph, balls, holes, ball_colour, hit_number):
        '''Responsible for adding the valid paths to the graph'''

        all_objects = balls + holes

        white_index = self.get_balls_index(balls, BallColour.White)
        target_indexes = self.get_balls_index(balls, ball_colour)

        possible_paths = list(itertools.combinations(target_indexes, hit_number))

        for entire_path in possible_paths:
            is_path_valid = False

            for i, a_ball in enumerate(entire_path):
                if i == 0:
                    is_path_valid = self.add_valid_edge(graph, None, white_index, a_ball, all_objects)
                else:
                    is_path_valid = self.add_valid_edge(graph, entire_path[i - 2], entire_path[i - 1], a_ball, all_objects)

                if not is_path_valid:
                    break

            if is_path_valid:
                for hole_index, _ in enumerate(holes):
                    if len(entire_path) == 1:
                        self.add_valid_edge(graph, white_index, entire_path[-1], (len(balls) + hole_index), all_objects)
                    else:
                        self.add_valid_edge(graph, entire_path[-2], entire_path[-1], (len(balls) + hole_index), all_objects)

    def add_valid_edge(self, graph, previous_index, start_index, end_index, all_objects):
        '''Adding an edge if there is nothing intercepting that path'''

        is_valid = self.is_path_ocluded(all_objects[start_index], all_objects[end_index], [start_index, end_index], all_objects)

        if is_valid:
            angle_weight = 0

            if previous_index is not None:
                angle = self.angle_between_three_points(all_objects[previous_index], all_objects[start_index], all_objects[end_index])

                if angle < self.min_angle or angle > self.max_angle:
                    return False

                if angle < 180:
                    angle_weight = (180 - angle) * 1000
                else:
                    angle_weight = (angle - 180) * 1000

            distance = self.distance_from_two_points(all_objects[start_index], all_objects[end_index])
            graph.add_edge(start_index, end_index, angle_weight + distance)

        return is_valid

    def is_path_ocluded(self, start_position, end_position, path_indexes, all_objects):
        '''Determine if path is ocluded by other balls'''

        line = self.line_equation_from_two_points(start_position, end_position)

        for ball_index, a_ball in enumerate(all_objects):
            if (ball_index not in path_indexes and len(a_ball) == 3):
                if not self.line_intercept_circle(line, a_ball, lookup.BALL_DIAMETER):
                    return False

        return True

    @staticmethod
    def get_balls_index(balls, ball_colour):
        '''Find balls which have a particular colour'''

        ball_colour_indexes = []

        for i, _ in enumerate(balls):
            if balls[i][2] is ball_colour:
                ball_colour_indexes.append(i)

        if (ball_colour is BallColour.White or ball_colour is BallColour.Black):
            if ball_colour_indexes:
                return ball_colour_indexes[0]

        return ball_colour_indexes

    @staticmethod
    def mid_point_from_two_points(point_one, point_two):
        '''Calculates the mid point between two points'''

        return ((point_one[0] + point_two[0]) / 2, (point_one[1] + point_two[1]) / 2)

    @staticmethod
    def distance_from_two_points(point_one, point_two):
        '''Calculates the distances between two points'''

        return math.sqrt(((point_one[0] - point_two[0]) ** 2) + ((point_one[1] - point_two[1]) ** 2))

    @staticmethod
    def angle_between_three_points(point_one, point_two, point_three):
        '''Calculate the angle between three points'''

        point_a = np.array([point_one[0], point_one[1]])
        point_b = np.array([point_two[0], point_two[1]])
        point_c = np.array([point_three[0], point_three[1]])

        vector_ba = point_a - point_b
        vector_bc = point_c - point_b

        cosine_angle = np.dot(vector_ba, vector_bc) / (np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc))

        return np.degrees(np.arccos(np.minimum(1, cosine_angle)))

    @staticmethod
    def line_equation_from_two_points(point_one, point_two):
        '''Returns line terms from two points'''

        l_a = point_one[1] - point_two[1]
        l_b = point_two[0] - point_one[0]
        l_c = (point_two[1] * point_one[0]) - (point_one[1] * point_two[0])

        return (l_a, l_b, l_c)

    @staticmethod
    def line_intercept_circle(line_terms, circle_point, circle_radius):
        '''Checks if a line intercepts a circle'''

        l_a = line_terms[0]
        l_b = line_terms[1]
        l_c = line_terms[2]

        c_x = circle_point[0]
        c_y = circle_point[1]

        distance = abs(l_a * c_x + l_b * c_y + l_c) / math.sqrt(l_a * l_a + l_b * l_b)

        return distance >= circle_radius
