# 8 Ball Pool Analysis

This is an Open Source project that analyses game footage from **[Miniclip's 8 ball pool](https://miniclip.com/games/8-ball-pool-multiplayer/en/)**.

It determines paths, which show the user a possibility of how the balls could be potted.

![animated.gif](../master/Assets/animated.gif)

## Installation

This tool uses standard image processing techniques through OpenCV, together with some vector algebra and graph logic.

```
pip install opencv-python
```

## Usage

This tool is run via the command-line, and contains various fine-tuning options, depending on the video input.

The current default values for ball and hole sizes were determined after rigorous testing, on a video from a 1080p display, with zoom and scaling set to 100%. As a result, videos which have been captured on displays with a different resolution, zoom and scaling might need further tweaking to obtain adequate results.

```
usage: start.py [-br N] [-hr N] [-bd N] [-tb type] [-ip file] [-op file] [-sf N] [-show] [-save] [-h]

This project analyses in game footage that indicates the optimal shot predictions using computer vision.

optional arguments:
  -br N, --ball_radius N         Radius of the pool balls (dependent on resolution, zooming and scaling).
  -hr N, --hole_radius N         Radius of the table holes (dependent on resolution, zooming and scaling).
  -bd N, --border_distance N     Distance from the centre of the holes to the outermost edge of the table.
  -tb type, --target_balls type  Choose ball type for path calculation.
  -ip file, --input_video file   File path containing the game footage to be analysed (*.MP4).
  -op file, --output_video file  File path for the output video (*.MP4).
  -sf N, --skip_frame N          Process a frame every N frame when analysing the video.
  -show, --show_video            Show the video while processing is being done.
  -save, --save_video            Save the video after the processing has finished.
  -h, --help                     Show this help message and exit.
```
