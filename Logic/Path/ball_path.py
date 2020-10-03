'''Ball Path Finding Handling Module'''

import math
import numpy as np

from Logic.Path.vectors import Vectors
from Logic.Detection.ball_colour import BallColour
from Logic.Path.dijkstra_graph import DijkstraGraph


class BallPath:
    ''' Responsible for finding an optimal path using dijkstra algorithm '''

    vectors = Vectors()

    def __init__(self, balls, holes, options):
        self.graph = DijkstraGraph()

        self.ball_colour = options.target_ball_colour

        self.white_index = self.get_balls_index(balls, BallColour.White)
        self.target_indices = [target_index for target_index in self.get_balls_index(balls, self.ball_colour)]

        self.balls = balls
        self.target_balls = [(balls[target_index][0], balls[target_index][1]) for target_index in self.target_indices]

        if self.white_index:
            self.white = balls[self.white_index]

        self.sorted_holes = sorted(holes, key=lambda tup: (-tup[1], tup[0]))
        self.sorted_holes[3::] = sorted(self.sorted_holes[3::], key=lambda tup: (-tup[0], tup[1]))

        self.target_holes = self.get_target_holes(options)
        self.all_objects = self.balls + self.target_holes

        self.shrink_borders = self.get_shrink_borders(options)

    def find_path(self, options):
        '''Responsible for calculating an optimal path for one hit'''

        if self.white_index and self.target_indices:
            self.add_graph_edges(options)

            hole_optimal_path = self.graph.find_any_goal_path(self.white, self.target_holes)

            if len(hole_optimal_path):
                return hole_optimal_path
            else:
                return self.graph.find_any_goal_path(self.white, self.target_balls)

        return []

    def add_graph_edges(self, options):
        '''Populating the graph with valid edges'''

        for target_hole_index, target_hole in enumerate(self.target_holes):
            for target_index in self.target_indices:
                target_ball_position = self.balls[target_index]
                target_hit_position = self.get_target_hit_position(target_index, target_hole_index, options)

                if target_hit_position is not None:
                    if self.is_path_valid(self.white, target_hit_position, [self.white_index, target_index], options):
                        if self.is_possible_shot(self.white, target_ball_position, target_hole, options):
                            distance = self.vectors.distance_from_two_points(self.white, target_hit_position)
                            self.graph.add_edge(self.white, target_hit_position, distance)

                            self.graph.add_edge(target_hit_position, target_ball_position, 0)
                            distance = self.vectors.distance_from_two_points(target_ball_position, target_hole)
                            self.graph.add_edge(target_ball_position, target_hole, distance)
                        else:
                            # When the shot is not possible the shortest distance between the white ball and the target ball is considered
                            # instead which adds a constant distance to make such paths less favourable than those that reach a hole

                            distance = self.vectors.distance_from_two_points(self.white, target_ball_position)
                            self.graph.add_edge(self.white, target_ball_position, distance + 10000)

    def get_target_hit_position(self, ball_index, hole_index, options):
        '''Responsible for calculating the target hit position'''

        ball = self.balls[ball_index]
        hole = self.target_holes[hole_index]

        line = self.vectors.line_from_two_points(ball, hole)

        for i, a_ball in enumerate(self.balls):
            # Line defines the path between two balls it is assumed to be blocked if
            # the distance less than two ball radii

            is_intercepted = self.vectors.line_intercept_circle(line, a_ball, options.ball_diameter)

            if i is not ball_index and is_intercepted:
                return None

        for i, _ in enumerate(self.sorted_holes):
            border_start = self.shrink_borders[((2 * i) + 1) % len(self.shrink_borders)]
            border_finish = self.shrink_borders[((2 * i) + 2) % len(self.shrink_borders)]

            if self.vectors.segment_intercept_from_four_points(ball, hole, border_start, border_finish):
                return None

        target_position = self.vectors.move_from_two_points(ball, hole, options.ball_radius * 2)

        if target_position is None:
            return None

        return target_position

    def is_path_valid(self, white_position, target_hit_position, exclude_indices, options):
        line = self.vectors.line_from_two_points(white_position, target_hit_position)

        for i, a_ball in enumerate(self.balls):
            # Line defines the path between two balls it is assumed to be blocked if
            # the distance less than two ball radii

            is_intercepted = self.vectors.line_intercept_circle(line, a_ball, int(options.ball_diameter))

            if i not in exclude_indices and is_intercepted:
                return False

        return True

    @staticmethod
    def is_possible_shot(white, target_ball, target_hole, options):
        lower_target_ball = (target_ball[0] - options.ball_diameter, target_ball[1] - options.ball_diameter)
        upper_target_ball = (target_ball[0] - options.ball_diameter, target_ball[1] - options.ball_diameter)

        lower_target_hole = (target_hole[0] - options.ball_diameter, target_hole[1] - options.ball_diameter)
        upper_target_hole = (target_hole[0] - options.ball_diameter, target_hole[1] - options.ball_diameter)

        not_valid_x = lower_target_ball[0] < white[0] < upper_target_hole[0] or lower_target_hole[0] < white[0] < upper_target_ball[0]
        not_valid_y = lower_target_ball[1] < white[1] < upper_target_hole[1] or lower_target_hole[1] < white[1] < upper_target_ball[1]

        return not (not_valid_x or not_valid_y)

    @staticmethod
    def get_balls_index(balls, ball_colour):
        '''Find balls which have a particular colour'''

        ball_colour_indices = []

        for i, _ in enumerate(balls):
            if balls[i][2] is ball_colour:
                ball_colour_indices.append(i)

        if (ball_colour is BallColour.White or ball_colour is BallColour.Black):
            if ball_colour_indices:
                return ball_colour_indices[0]

        return ball_colour_indices

    def get_target_holes(self, options):
        '''Finding the target holes which are used to score a ball'''

        target_holes = []

        start_angle = 3 * math.pi / 16
        finish_angle = 5 * math.pi / 16

        frequency = 5
        angle_step = np.linspace(start_angle, finish_angle, frequency, True)

        for i, angle in enumerate(angle_step):
            minor_cos_angle = int(options.middle_hole_radius * math.cos(angle + (math.pi / 4)))
            minor_sin_angle = int(options.middle_hole_radius * math.sin(angle + (math.pi / 4)))

            major_cos_angle = int(options.corner_hole_radius * math.cos(angle))
            major_sin_angle = int(options.corner_hole_radius * math.sin(angle))

            target_holes.append((self.sorted_holes[0][0] + major_cos_angle, self.sorted_holes[0][1] - major_sin_angle))
            target_holes.append((self.sorted_holes[2][0] - major_cos_angle, self.sorted_holes[2][1] - major_sin_angle))
            target_holes.append((self.sorted_holes[3][0] - major_cos_angle, self.sorted_holes[3][1] + major_sin_angle))
            target_holes.append((self.sorted_holes[5][0] + major_cos_angle, self.sorted_holes[5][1] + major_sin_angle))

            target_holes.append((self.sorted_holes[1][0] - minor_cos_angle, self.sorted_holes[1][1] - minor_sin_angle))
            target_holes.append((self.sorted_holes[4][0] + minor_cos_angle, self.sorted_holes[4][1] + minor_sin_angle))

        return target_holes

    def get_shrink_borders(self, options):
        '''Responsible for shrinking the game border'''

        minor_scale = options.middle_border_radius
        major_scale = options.corner_border_radius

        middle_scale = int(minor_scale * 2)

        hole_00 = (self.sorted_holes[0][0] + minor_scale, self.sorted_holes[0][1] - major_scale)
        hole_01 = (self.sorted_holes[0][0] + major_scale, self.sorted_holes[0][1] - minor_scale)

        hole_10 = (self.sorted_holes[1][0] - middle_scale, self.sorted_holes[1][1] - minor_scale)
        hole_11 = (self.sorted_holes[1][0] + middle_scale, self.sorted_holes[1][1] - minor_scale)

        hole_20 = (self.sorted_holes[2][0] - major_scale, self.sorted_holes[2][1] - minor_scale)
        hole_21 = (self.sorted_holes[2][0] - minor_scale, self.sorted_holes[2][1] - major_scale)

        hole_30 = (self.sorted_holes[3][0] - minor_scale, self.sorted_holes[3][1] + major_scale)
        hole_31 = (self.sorted_holes[3][0] - major_scale, self.sorted_holes[3][1] + minor_scale)

        hole_40 = (self.sorted_holes[4][0] + middle_scale, self.sorted_holes[4][1] + minor_scale)
        hole_41 = (self.sorted_holes[4][0] - middle_scale, self.sorted_holes[4][1] + minor_scale)

        hole_50 = (self.sorted_holes[5][0] + major_scale, self.sorted_holes[5][1] + minor_scale)
        hole_51 = (self.sorted_holes[5][0] + minor_scale, self.sorted_holes[5][1] + major_scale)

        return [hole_00, hole_01, hole_10, hole_11, hole_20, hole_21, hole_30, hole_31, hole_40, hole_41, hole_50, hole_51]
