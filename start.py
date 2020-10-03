'''Start Module'''

import argparse

from Logic.options import Options
from Logic.video_analysis import VideoAnalysis


def create_parser():
    '''Responsible for creating a parser that handles program arguments'''

    formatter = lambda prog: argparse.HelpFormatter(prog, width=140, max_help_position=50)

    parser = argparse.ArgumentParser(
        description='This project analyses in game footage that indicates the optimal shot predictions using computer vision.',
        formatter_class=formatter,
        add_help=False
    )

    parser.add_argument('-br', '--ball_radius', metavar='N', type=int, nargs=1, default=[10], help='Radius of the pool balls (dependent on resolution, zooming and scaling).')
    parser.add_argument('-hr', '--hole_radius', metavar='N', type=int, nargs=1, default=[20], help='Radius of the table holes (dependent on resolution, zooming and scaling).')
    parser.add_argument('-bd', '--border_distance', metavar='N', type=int, nargs=1, default=[15], help='Distance from the centre of the holes to the outermost edge of the table.')

    parser.add_argument('-tb', '--target_balls', metavar='type', type=str, nargs=1, choices=['solid', 'striped'], default=['solid'], help='Choose ball type for path calculation.')

    parser.add_argument('-ip', '--input_video', metavar='file', type=str, nargs=1, default='Footage\\Example_01.mp4', help='File path containing the game footage to be analysed (*.MP4).')
    parser.add_argument('-op', '--output_video', metavar='file', type=str, nargs=1, default='Footage\\Output.mp4', help='File path for the output video (*.MP4).')

    parser.add_argument('-sf', '--skip_frame', metavar='N', type=int, nargs=1, default=[10], help='Process a frame every N frame when analysing the video.')

    parser.add_argument('-show', '--show_video', action='store_true', help='Show the video while processing is being done.')
    parser.add_argument('-save', '--save_video', action='store_true', help='Save the video after the processing has finished.')

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    options = Options(args)

    video_analysis = VideoAnalysis()
    video_analysis.analyse_video(options)
