'''Detection Training Module'''

import os
import numpy as np
import cv2

import Config.eight_ball_lookup as lookup

from Logic.bot import Bot
from Logic.item_detection import ItemDetection
from Logic.item_classification import ItemClassification

class DetectionTraining:
    '''Responisble for handling detection training'''

    item_detection = ItemDetection()
    item_classification = ItemClassification()

    def identify_parameters(self, identify_for_holes, identify_for_balls):
        '''Iterating through a number of images and saving the image results based on different parameter values'''

        for files in os.listdir(lookup.TRAINING_FOLDER):
            image_path = os.path.join(lookup.TRAINING_FOLDER, files)

            if (os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                if identify_for_holes:
                    if not os.path.exists(lookup.HOLE_TRAINING_PATH):
                        os.makedirs(lookup.HOLE_TRAINING_PATH)

                    self.find_hole_parameters(image_path)

                if identify_for_balls:
                    if not os.path.exists(lookup.BALL_TRAINING_PATH):
                        os.makedirs(lookup.BALL_TRAINING_PATH)

                    hole_positions = self.item_detection.find_holes(image_path)
                    self.find_ball_parameters(image_path, hole_positions)

    @staticmethod
    def find_hole_parameters(image_path):
        '''Iterate through a range of values and saving each result in the aim of identifying the best parameters for hole detection'''

        for param2 in range(13, 17, 1):
            for param1 in range(10, 310, 10):
                print('Hole Parameters:', param1, param2)

                rgb_image = cv2.imread(image_path)
                gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

                holes = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 10, param1=param1, param2=param2, minRadius=20, maxRadius=21)

                if holes is not None:
                    holes = np.round(holes[0, :]).astype("int")

                    for (x_position, y_position, _) in holes:
                        cv2.circle(rgb_image, (x_position, y_position), 2, (15, 10, 25), 3)
                        cv2.circle(rgb_image, (x_position, y_position), lookup.BALL_RADIUS, (25, 10, 255), 3)

                cv2.imwrite(lookup.HOLE_TRAINING_PATH + str(param2) + '_' + str(param1) + '.jpg', rgb_image)

    def find_ball_parameters(self, image_path, hole_positions):
        '''Iterate through a range of values and saving each result in the goal of identify the best parameters for ball detection'''

        board_positions = self.item_detection.board_boundary(hole_positions)

        for param2 in range(13, 17, 1):
            for param1 in range(10, 310, 10):
                print('Ball Parameters:', param1, param2)

                rgb_image = cv2.imread(image_path)
                board_frame = rgb_image[board_positions[1]:board_positions[3], board_positions[0]:board_positions[2]]

                board_frame_edges = cv2.Canny(board_frame, 200, 300)

                circles = cv2.HoughCircles(board_frame_edges, cv2.HOUGH_GRADIENT, 1, 9, param1=param1, param2=param2, minRadius=7, maxRadius=13)

                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")

                    for (x_position, y_position, _) in circles:
                        cv2.circle(rgb_image, (board_positions[0] + x_position, board_positions[1] + y_position), 2, (15, 10, 25), 3)
                        cv2.circle(rgb_image, (board_positions[0] + x_position, board_positions[1] + y_position), lookup.BALL_RADIUS, (25, 10, 255), 3)

                cv2.imwrite(lookup.BALL_TRAINING_PATH + str(param2) + '_' + str(param1) + '.jpg', rgb_image)

    def detection_on_video(self, video_path, show_video, save_video):
        '''Responsible for molding the features implemented on a given video which can be displayed or saved'''

        bot = Bot()
        frame_count = 0

        cap = cv2.VideoCapture(video_path)

        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 30, (1920, 1080))

        while cap.isOpened():
            frame_count += 1
            ret, frame = cap.read()

            if not bot.holes:
                bot.find_holes(frame)

            if ret:
                modified_frame = frame.copy()

                self.print_timestamp(frame_count)

                bot.find_balls(frame)

                for hole in bot.holes:
                    cv2.circle(modified_frame, (hole[0], hole[1]), 2, (255, 255, 255), 3)
                    cv2.circle(modified_frame, (hole[0], hole[1]), 20, (255, 255, 255), 3)

                for ball in bot.balls:
                    rgb_colour = None
                    ball_pixels = self.item_classification.get_ball_pixels(frame, ball)

                    white_count = self.item_classification.get_white_count(ball_pixels)
                    black_count = self.item_classification.get_black_count(ball_pixels)

                    if self.item_classification.is_solid_ball(white_count, black_count):
                        rgb_colour = (255, 0, 0)
                    elif self.item_classification.is_stripped_ball(white_count, black_count):
                        rgb_colour = (0, 255, 0)
                    elif self.item_classification.is_black_ball(white_count, black_count):
                        rgb_colour = (255, 255, 0)
                    elif self.item_classification.is_white_ball(white_count):
                        rgb_colour = (0, 255, 255)

                    if rgb_colour is not None:
                        cv2.circle(modified_frame, (ball[0], ball[1]), 2, (0, 0, 0), 3)
                        cv2.circle(modified_frame, (ball[0], ball[1]), lookup.BALL_RADIUS, rgb_colour, 3)

                if save_video:
                    out.write(modified_frame)

                if show_video:
                    cv2.imshow('Object Detection', modified_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                break

        if save_video:
            out.release()

    @staticmethod
    def print_timestamp(frame_count):
        '''Responsible for outputting a timestamp based the frame count'''

        if frame_count % 30 == 0:
            time_hours = int(frame_count / 108000)
            time_minutes = int(frame_count / 1800) % 60
            time_seconds = int((frame_count % 1800) / 30)

            print('Current Timestamp: ' + str(time_hours) + ':' + str(time_minutes) + ':' + str(time_seconds))
