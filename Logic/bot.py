'''Bot Handling Module'''

import cv2

from Logic.item_detection import ItemDetection

class Bot:
    '''Responsible for handling the 8 ball game bot'''

    balls = []
    holes = []

    item_detection = ItemDetection()

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
            self.update_ball_positions(board_positions, detected_balls)

    def update_ball_positions(self, board_positions, detected_balls):
        '''Responsible for updating the ball positions to map from board coordinates to entire frame coordinates'''

        self.balls = []

        for ball in detected_balls:
            if ball is not None:
                self.balls.append((ball[0] + board_positions[0], ball[1] + board_positions[1]))
