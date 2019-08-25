'''Item Detection Module'''

import os
import numpy as np
import cv2

from skimage.measure import compare_ssim as ssim

from Config.eight_ball_lookup import EightBallLookup

class ItemDetection:
    '''Responsible for detecting game balls and holes'''

    lookup = EightBallLookup()

    def identify_parameters(self, for_holes, for_balls):
        '''Responsible iterating through a number of images and saving the image results based on different parameter values'''

        for ball_folder in os.listdir(self.lookup.training_path):
            ball_path = os.path.join(self.lookup.training_path, ball_folder)

            if (os.path.isfile(ball_path) and ball_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
                if for_holes:
                    if not os.path.exists(self.lookup.hole_training_path):
                        os.makedirs(self.lookup.hole_training_path)

                    self.find_hole_parameters(ball_path)

                if for_balls:
                    if not os.path.exists(self.lookup.ball_training_path):
                        os.makedirs(self.lookup.ball_training_path)

                    hole_positions = self.detect_holes(ball_path)
                    self.find_ball_parameters(ball_path, hole_positions)

    def find_hole_parameters(self, image_path):
        '''Iterate through a range of values and saving each result in the aim of identifying the best parameters for hole detection'''

        for param2 in range(13, 17, 1):
            for param1 in range(10, 310, 10):
                print('Hole Parameters:', param1, param2)

                rgb_image = cv2.imread(image_path)
                gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

                holes = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 10, param1=param2, param2=param2, minRadius=20, maxRadius=21)

                if holes is not None:
                    holes = np.round(holes[0, :]).astype("int")

                    for (x_position, y_position, radius) in holes:
                        cv2.circle(rgb_image, (x_position, y_position), 2, (15, 10, 25), 3)
                        cv2.circle(rgb_image, (x_position, y_position), radius, (25, 10, 255), 3)

                cv2.imwrite(self.lookup.hole_training_path + str(param2) + '_' + str(param1) + '.jpg', rgb_image)

    def find_ball_parameters(self, image_path, hole_positions):
        '''Iterate through a range of values and saving each result in the goal of identify the best parameters for ball detection'''

        min_x = min(hole_positions, key=lambda t: t[0])[0] + 10
        min_y = min(hole_positions, key=lambda t: t[1])[1] + 10
        max_x = max(hole_positions, key=lambda t: t[0])[0] - 10
        max_y = max(hole_positions, key=lambda t: t[1])[1] - 10

        for param2 in range(13, 17, 1):
            for param1 in range(10, 310, 10):
                print('Ball Parameters:', param1, param2)

                marker_image = cv2.imread(self.lookup.marker)
                marker_image = cv2.cvtColor(marker_image, cv2.COLOR_BGR2GRAY)

                rgb_image = cv2.imread(image_path)
                gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

                circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 10, param1=param1, param2=param2, minRadius=9, maxRadius=13)

                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")

                    for (x_position, y_position, radius) in circles:
                        radius = 13 # assuming ball is always 13 pixels

                        if min_x <= x_position and x_position <= max_x and min_y <= y_position and y_position < max_y:
                            check_image = gray_image[(y_position - radius) : (y_position + radius), (x_position - radius) : (x_position + radius)]

                            if ssim(check_image, marker_image) < 0:
                                cv2.circle(rgb_image, (x_position, y_position), 2, (15, 10, 25), 3)
                                cv2.circle(rgb_image, (x_position, y_position), radius, (25, 10, 255), 3)

                cv2.imwrite(self.lookup.ball_training_path + str(param2) + '_' + str(param1) + '.jpg', rgb_image)

    def detect_holes(self, frame):
        '''Responsible for returning an array of hole positions'''

        detected_holes = []

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        holes = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=16, minRadius=20, maxRadius=21)

        if holes is not None:
            holes = np.round(holes[0, :]).astype("int")

            for (x_position, y_position, radius) in holes:
                detected_holes.append((x_position, y_position))

        return detected_holes

    def detect_balls(self, frame, hole_positions):
        '''Responsible for returning an array of ball positions'''

        detected_circles = []

        min_x = min(hole_positions, key=lambda t: t[0])[0] + 10
        min_y = min(hole_positions, key=lambda t: t[1])[1] + 10
        max_x = max(hole_positions, key=lambda t: t[0])[0] - 10
        max_y = max(hole_positions, key=lambda t: t[1])[1] - 10

        marker_image = cv2.imread(self.lookup.marker)
        marker_image = cv2.cvtColor(marker_image, cv2.COLOR_BGR2GRAY)

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 9, param1=300, param2=15, minRadius=9, maxRadius=13)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (x_position, y_position, radius) in circles:
                radius = 13 # assuming ball is always 13 pixels

                if min_x <= x_position and x_position <= max_x and min_y <= y_position and y_position < max_y:
                    check_image = gray_image[(y_position - radius) : (y_position + radius), (x_position - radius) : (x_position + radius)]

                    if ssim(check_image, marker_image) < 0:
                        detected_circles.append((x_position, y_position))

        return detected_circles

    def detection_video(self, video_path, show_video, record_video):
        '''Responsible for molding the features implemented on a given video which can be displayed or saved'''

        cap = cv2.VideoCapture(video_path)

        if record_video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 30, (1920, 1080))

        holes = []
        frame_count = 0

        while cap.isOpened():
            frame_count += 1
            ret, frame = cap.read()

            if frame_count % 30 == 0: # Assuming footage is recorded at 30 fps
                time_hours = int(frame_count / 108000)
                time_minutes = int(frame_count / 1800) % 60
                time_seconds = int((frame_count % 1800) / 30)

                print('Current Timestamp: ' + str(time_hours) + ':' + str(time_minutes) + ':' + str(time_seconds))

            if not holes: # Only detect the balls once
                holes = self.detect_holes(frame)

                min_x = min(holes, key=lambda t: t[0])[0]
                min_y = min(holes, key=lambda t: t[1])[1]
                max_x = max(holes, key=lambda t: t[0])[0]
                max_y = max(holes, key=lambda t: t[1])[1]

                holes.append((int(min_x + ((max_x - min_x) / 2)), min_y))
                holes.append((int(min_x + ((max_x - min_x) / 2)), max_y))

            if ret:
                balls = self.detect_balls(frame, holes)

                for hole in holes:
                    cv2.circle(frame, (hole[0], hole[1]), 2, (15, 10, 25), 3)
                    cv2.circle(frame, (hole[0], hole[1]), 20, (25, 10, 255), 3)

                for ball in balls:
                    cv2.circle(frame, (ball[0], ball[1]), 2, (15, 10, 25), 3)
                    cv2.circle(frame, (ball[0], ball[1]), 13, (25, 10, 255), 3)

                if record_video:
                    out.write(frame)

                if show_video:
                    cv2.imshow('Object Detection', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                break

        if record_video:
            out.release()
