'''Bot Handling Module'''

import cv2

from Logic.ball_path import BallPath
from Logic.ball_colour import BallColour
from Logic.item_detection import ItemDetection
from Logic.item_classification import ItemClassification

class Bot:
    '''Responsible for handling the 8 ball game bot'''

    balls = []
    holes = []

    target_ball_colour = BallColour.Solid

    ball_path = BallPath()
    item_detection = ItemDetection()
    item_classification = ItemClassification()

    def find_holes(self, frame):
        '''Responsible for finding the holes if not set'''

        if not self.holes:
            self.holes = self.item_detection.find_holes(frame)

            board_positions = self.item_detection.board_boundary(self.holes)

            self.holes.append((int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[1]))
            self.holes.append((int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[3]))

    def find_balls(self, frame):
        '''Responsible for finding the balls'''

        board_positions = self.item_detection.board_boundary(self.holes)

        board_frame = frame[board_positions[1]:board_positions[3], board_positions[0]:board_positions[2]]
        board_frame_edges = cv2.Canny(board_frame, 200, 300)

        detected_balls = self.item_detection.find_balls(board_frame_edges)

        if len(detected_balls) < 18:
            self.update_ball_structure(frame, board_positions, detected_balls)

    def update_ball_structure(self, frame, board_positions, detected_balls):
        '''Responsible for handling updating the ball structure to assist the bot'''

        self.balls = []

        for ball in detected_balls:
            if ball is not None:
                new_ball_position = self.update_ball_positions(board_positions, ball)
                ball_colour = self.classify_ball_colours(frame, new_ball_position)

                self.balls.append((new_ball_position[0], new_ball_position[1], ball_colour))

    @staticmethod
    def update_ball_positions(board_positions, detected_ball):
        '''Responsible for updating the ball position to map from board coordinates to entire frame coordinates'''

        return (detected_ball[0] + board_positions[0], detected_ball[1] + board_positions[1])

    def classify_ball_colours(self, frame, detected_ball):
        '''Responsible for classifying a ball'''

        ball_colour = None

        ball_pixels = self.item_classification.get_ball_pixels(frame, detected_ball)

        white_count = self.item_classification.get_white_count(ball_pixels)
        black_count = self.item_classification.get_black_count(ball_pixels)

        if self.item_classification.is_solid_ball(white_count, black_count):
            ball_colour = BallColour.Solid
        elif self.item_classification.is_striped_ball(white_count, black_count):
            ball_colour = BallColour.Strip
        elif self.item_classification.is_black_ball(white_count, black_count):
            ball_colour = BallColour.Black
        elif self.item_classification.is_white_ball(white_count):
            ball_colour = BallColour.White

        return ball_colour

    def find_optimal_path(self):
        '''Responsible for initiating the find optimal path method'''

        hit_number = 1
        optimal_path = []

        all_objects = self.balls + self.holes
        found_valid_path = False

        while (not found_valid_path and hit_number != 3):
            optimal_path = self.ball_path.find_path(self.balls, self.holes, self.target_ball_colour, hit_number)

            if len(optimal_path) > 2:
                found_valid_path = True
            else:
                hit_number += 1

        if not found_valid_path:
            optimal_path = self.ball_path.find_valid_hit(self.balls, self.holes, self.target_ball_colour)

        for i, path in enumerate(optimal_path):
            if not hasattr(path, "__len__"):
                optimal_path[i] = (all_objects[path][0], all_objects[path][1])

        return optimal_path
