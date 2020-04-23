# Installation
Best to work in a `venv` before installing the requirements in `req.txt`:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r req.txt
```

# Usage
Upload your videos to `videos/` folder in the `gimme_mov` directory.

Call `main.py`, using the `--vid_dir` flag to point to your directory of videos. It defaults to `./videos/`.

```
python3 main.py --vid_dir ./videos/
```