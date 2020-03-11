'''Ball Detection Module'''

import numpy as np
import cv2


class BallDetection:
    '''Responsible for detecting game balls and holes'''

    @staticmethod
    def board_boundary(holes):
        '''Responsible for returning the boundary of the board'''

        min_x = min(holes, key=lambda t: t[0])[0]
        min_y = min(holes, key=lambda t: t[1])[1]
        max_x = max(holes, key=lambda t: t[0])[0]
        max_y = max(holes, key=lambda t: t[1])[1]

        return [min_x, min_y, max_x, max_y]

    @staticmethod
    def find_corner_holes(entire_frame):
        '''Responsible for returning an array of hole positions'''

        detected_holes = []

        gray_image = cv2.cvtColor(entire_frame, cv2.COLOR_BGR2GRAY)

        holes = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=16, minRadius=20, maxRadius=21)

        if holes is not None:
            holes = np.round(holes[0, :]).astype("int")

            for (x_position, y_position, _) in holes:
                detected_holes.append((x_position, y_position))

        return detected_holes

    @staticmethod
    def find_balls(board_frame_edges):
        '''Responsible for returning an array of ball positions'''

        detected_balls = []

        circles = cv2.HoughCircles(board_frame_edges, cv2.HOUGH_GRADIENT, 1, 9, param1=300, param2=15, minRadius=7, maxRadius=13)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (x_position, y_position, _) in circles:
                detected_balls.append((x_position, y_position))

        return detected_balls
