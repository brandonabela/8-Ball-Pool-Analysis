'''Options Module'''

from Logic.Detection.ball_colour import BallColour


class Options:
    def __init__(self, args):
        self.ball_radius = args.ball_radius[0]
        self.ball_diameter = args.ball_radius[0] * 2.2

        self.hole_radius = args.hole_radius[0]
        self.border_distance = args.border_distance[0]

        self.middle_hole_radius = int(args.border_distance[0] * 1.2)
        self.corner_hole_radius = int(args.border_distance[0] * 2.6)

        self.middle_border_radius = int(args.border_distance[0] * 0.8)
        self.corner_border_radius = int(args.border_distance[0] * 2.8)

        self.target_ball_colour = BallColour.Solid if args.target_balls[0] == 'solid' else BallColour.Strip

        self.input_video = args.input_video
        self.output_video = args.output_video

        self.skip_frame = args.skip_frame[0]

        self.show_video = args.show_video
        self.save_video = args.save_video
