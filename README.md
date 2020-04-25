# Installation
Best to work in a `venv` before installing the requirements in `req.txt`:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r req.txt
```

# Usage
Upload videos into the `./videos/` directory, then call `main.py`
```
python3 main.py
```

# Options
- `--vid_dir` - the path to the video directory, defaults to `./videos/`
- `--vid_mul` - how many times you want the videos to be repeated, defaults to `1`
- `--begin` - a comma separated list of videos to begin with
  - e.x. `--begin ./videos/video_1.mov,./videos/video_2.mov`
- `--end` - a comma separated list of videos to end with
  - e.x. `--end ./videos/2nd_to_last,./videos/last.mov`
- `--shuffle` - whether to shuffle the video order (except for videos denoted by `begin` and `end`), this is `True` by default
- `--output` - the name of the output file, defaults to `output.mp4` in the directory denoted by `vid_dir`
- `--vid_len` - length of the video, defaults to `59.7` seconds (just under Instagram video time limits)
- `--square` - whether to put a white square border around the video (useful for sharing as a post instead of a story), defaults to `True`
- `--audio` - the audio to put over the video, defaults to `gimme_trim.m4a`