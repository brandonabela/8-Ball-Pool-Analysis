'''Bot Handling Module'''

import cv2

from Logic.Path.vectors import Vectors
from Logic.Path.ball_path import BallPath
from Logic.Detection.ball_colour import BallColour
from Logic.Detection.ball_detection import BallDetection
from Logic.Detection.ball_classification import BallClassification


class Bot:
    '''Responsible for handling the 8 ball game bot'''

    balls = []
    holes = []

    vector = Vectors()
    ball_detection = BallDetection()
    ball_classification = BallClassification()

    def find_holes(self, frame):
        '''Responsible for finding the holes if not set'''

        if not self.holes:
            corner_holes = self.ball_detection.find_corner_holes(frame)

            if len(corner_holes) == 4:
                self.holes = corner_holes

                board_positions = self.ball_detection.board_boundary(self.holes)

                self.holes.append((int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[1]))
                self.holes.append((int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[3]))

    def find_balls(self, frame, options):
        '''Responsible for finding the balls'''

        board_positions = self.ball_detection.board_boundary(self.holes)

        board_frame = frame[board_positions[1]:board_positions[3], board_positions[0]:board_positions[2]]
        board_frame_edges = cv2.Canny(board_frame, 200, 300)

        detected_balls = self.ball_detection.find_balls(board_frame_edges)

        if len(detected_balls) < 18:
            self.update_ball_structure(frame, board_positions, detected_balls, options)

    def update_ball_structure(self, frame, board_positions, detected_balls, options):
        '''Responsible for handling updating the ball structure to assist the bot'''

        self.balls = []

        for ball in detected_balls:
            if ball is not None:
                new_ball_position = self.update_ball_positions(board_positions, ball)
                ball_colour = self.classify_ball_colours(frame, new_ball_position, options)

                self.balls.append((int(new_ball_position[0]), int(new_ball_position[1]), ball_colour))

    @staticmethod
    def update_ball_positions(board_positions, detected_ball):
        '''Responsible for updating the ball position to map from board coordinates to entire frame coordinates'''

        return detected_ball[0] + board_positions[0], detected_ball[1] + board_positions[1]

    def classify_ball_colours(self, frame, detected_ball, options):
        '''Responsible for classifying a ball'''

        ball_colour = None

        ball_pixels = self.ball_classification.get_ball_pixels(frame, detected_ball, options)

        white_count = self.ball_classification.get_white_count(ball_pixels)
        black_count = self.ball_classification.get_black_count(ball_pixels)

        if self.ball_classification.is_solid_ball(white_count, black_count):
            ball_colour = BallColour.Solid
        elif self.ball_classification.is_striped_ball(white_count, black_count):
            ball_colour = BallColour.Strip
        elif self.ball_classification.is_black_ball(white_count, black_count):
            ball_colour = BallColour.Black
        elif self.ball_classification.is_white_ball(white_count):
            ball_colour = BallColour.White

        return ball_colour

    def find_optimal_path(self, options):
        '''Responsible for initiating the find optimal path method'''

        optimal_path = []
        all_objects = self.balls + self.holes

        ball_path = BallPath(self.balls, self.holes, options)
        optimal_path = ball_path.find_path(options)

        return optimal_path
