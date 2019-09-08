'''Bot Handling Module'''

import cv2

from Logic.item_detection import ItemDetection

class Bot:
    '''Responsible for handling the 8 ball game bot'''

    balls = []
    holes = []

    initial_balls_found = False

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

        self.balls = self.item_detection.find_balls(board_frame_edges)
        self.update_ball_positions(board_positions)

    def update_ball_positions(self, board_positions):
        '''Responsible for updating the ball positions to map from board coordinates to entire frame coordinates'''

        for ball in self.balls:
            if ball is not None:
                ball[0] += board_positions[0]
                ball[1] += board_positions[1]
