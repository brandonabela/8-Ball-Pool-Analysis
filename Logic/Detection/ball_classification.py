'''Ball Classification Module'''

import math


class BallClassification:
    '''Responsible for classifying game balls'''

    @staticmethod
    def get_ball_radius(x_position, y_position, options):
        '''Calculate radius from ball point'''

        return math.sqrt(math.pow(options.ball_radius - x_position, 2) + math.pow(options.ball_radius - y_position, 2))

    def get_ball_pixels(self, frame, position, options):
        '''Responsible for returning an array of pixels that represent the circle'''

        ball_pixels = []

        min_x_position = int(position[0] - options.ball_radius)
        min_y_position = int(position[1] - options.ball_radius)
        max_x_position = int(position[0] + options.ball_radius)
        max_y_position = int(position[1] + options.ball_radius)

        ball_frame = frame[min_y_position:max_y_position, min_x_position:max_x_position].copy()

        for x_position, _ in enumerate(ball_frame[0:-1]):
            for y_position, _ in enumerate(ball_frame[0:-1]):
                if self.get_ball_radius(x_position, y_position, options) < options.ball_radius:
                    ball_pixels.append(ball_frame[x_position][y_position])

        return ball_pixels

    @staticmethod
    def get_white_count(ball_pixels):
        '''Finding the number of white pixels within the ball pixels'''

        white_count = 0

        for pixel in ball_pixels:
            is_b_valid = 192 <= pixel[0] <= 255
            is_g_valid = 192 <= pixel[1] <= 255
            is_r_valid = 192 <= pixel[2] <= 255

            if is_b_valid and is_g_valid and is_r_valid:
                white_count += 1

        return white_count

    @staticmethod
    def get_black_count(ball_pixels):
        '''Finding the number of black pixels within the ball pixels'''

        black_count = 0

        for pixel in ball_pixels:
            is_b_valid = 0 <= pixel[0] <= 64
            is_g_valid = 0 <= pixel[1] <= 64
            is_r_valid = 0 <= pixel[2] <= 64

            if is_b_valid and is_g_valid and is_r_valid:
                black_count += 1

        return black_count

    @staticmethod
    def is_solid_ball(white_count, black_count):
        '''Checking whether the pixel count is a solid ball'''

        return 7 <= white_count <= 72 and 0 <= black_count <= 41

    @staticmethod
    def is_striped_ball(white_count, black_count):
        '''Checking whether the pixel count is a striped ball'''

        return 73 <= white_count <= 159 and 0 <= black_count <= 58

    @staticmethod
    def is_black_ball(white_count, black_count):
        '''Checking whether the pixel count is a black ball'''

        return (7 <= white_count <= 38 and 131 <= black_count <= 177) or (73 <= white_count <= 159 and 83 <= black_count <= 99)

    @staticmethod
    def is_white_ball(white_count):
        '''Checking whether the pixel count is a white ball'''

        return 160 <= white_count <= 238
